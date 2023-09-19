from abc import abstractmethod
import enum
from typing import ClassVar, Iterable, List, Optional, Tuple

from trulens_eval.feedback.provider.endpoint.base import Endpoint
from trulens_eval.utils.generated import re_1_10_rating
from trulens_eval.utils.pyschema import WithClassInfo
from trulens_eval.utils.serial import SerialModel
from cohere.responses.classify import Example
from langchain.evaluation.criteria.eval_chain import _SUPPORTED_CRITERIA
from langchain import PromptTemplate
import pydantic
from pydantic import Field

# Level 1 abstraction

def make_retab(tab):
    def retab(s):
        lines = s.split("\n")
        return tab + f"\n{tab}".join(lines)
    return retab

class WithExamples(pydantic.BaseModel):
    examples: ClassVar[List[Example]]

class WithPrompt(pydantic.BaseModel):
    prompt: ClassVar[PromptTemplate]

class Feedback(pydantic.BaseModel):
    """
    Base class for feedback functions.
    """

    @classmethod
    def help(cls):
        print(cls.str_help())

    @classmethod
    def str_help(cls):
        typ = cls

        ret = typ.__name__ + "\n"

        fields = list(f for f in cls.__fields__ if f not in ["examples", "prompt"])

        onetab = make_retab("   ")
        twotab = make_retab("      ")

        # feedback hierarchy location
        for parent in typ.__mro__[::-1]:
            if parent == typ:
                continue

            if not issubclass(parent, Feedback):
                continue

            ret += onetab(f"Subtype of {parent.__name__}.") + "\n"

            for f in list(fields):
                if f in parent.__fields__:
                    fields.remove(f)
                    if hasattr(cls, f):
                        ret += twotab(f"{f} = {getattr(cls, f)}") + "\n"
                    else:
                        ret += twotab(f"{f} = instance specific") + "\n"
        
        if hasattr(typ, "__doc__") and typ.__doc__ is not None:
            ret += "\nDocstring\n"
            ret += onetab(typ.__doc__) + "\n"

        if issubclass(cls, WithExamples):
            ret += "\nExamples:\n"
            for e in cls.examples:
                ret += onetab(str(e)) + "\n"

        if issubclass(cls, WithPrompt):
            ret += f"\nPrompt: of {cls.prompt.input_variables}\n"
            ret += onetab(cls.prompt.template) + "\n"
        
        return ret
    
    pass

class NaturalLanguage(Feedback):
    languages: Optional[List[str]] = None
    

class Syntax(NaturalLanguage):
    pass

class LanguageMatch(Syntax):
    # hugs.language_match
    pass

class Semantics(NaturalLanguage):
    pass

class GroundTruth(Semantics):
    # Some groundtruth may also be syntactic if it merely compares strings
    # without interpretation by some model like these below:

    # GroundTruthAgreement.bert_score
    # GroundTruthAgreement.bleu
    # GroundTruthAgreement.rouge
    # GroundTruthAgreement.agreement_measure
    pass

supported_criteria = {
    key: value.replace(" If so, response Y. If not, respond N.", '')
    if isinstance(value, str) else value
    for key, value in _SUPPORTED_CRITERIA.items()
}

class Conciseness(Semantics, WithPrompt): # or syntax?
    # openai.conciseness

    # langchain Criteria.CONCISENESS
    prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template(
        f"""{supported_criteria['conciseness']} Respond only as a number from 1 to 10 where 1 is the least concise and 10 is the most concise."""
    )


class Correctness(Semantics, WithPrompt):
    # openai.correctness
    # openai.correctness_with_cot_reasons

    # langchain Criteria.CORRECTNESS
    prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template(
        f"""{supported_criteria['correctness']} Respond only as a number from 1 to 10 where 1 is the least correct and 10 is the most correct."""
    )

class Coherence(Semantics):
    # openai.coherence
    # openai.coherence_with_cot_reasons

    prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template(
        f"""{supported_criteria['coherence']} Respond only as a number from 1 to 10 where 1 is the least coherent and 10 is the most coherent."""
    )
    
class Relevance(Semantics):
    """
This evaluates the *relevance* of the LLM response to the given text by LLM
prompting.

Relevance is currently only available with OpenAI ChatCompletion API.

TruLens offers two particular flavors of relevance: 1. *Prompt response
relevance* is best for measuring the relationship of the final answer to the
user inputed question. This flavor of relevance is particularly optimized for
the following features:

    * Relevance requires adherence to the entire prompt.
    * Responses that don't provide a definitive answer can still be relevant
    * Admitting lack of knowledge and refusals are still relevant.
    * Feedback mechanism should differentiate between seeming and actual
      relevance.
    * Relevant but inconclusive statements should get increasingly high scores
      as they are more helpful for answering the query.

    You can read more information about the performance of prompt response
    relevance by viewing its [smoke test results](../pr_relevance_smoke_tests/).

2. *Question statement relevance*, sometimes known as context relevance, is best
   for measuring the relationship of a provided context to the user inputed
   question. This flavor of relevance is optimized for a slightly different set
   of features:
    * Relevance requires adherence to the entire query.
    * Long context with small relevant chunks are relevant.
    * Context that provides no answer can still be relevant.
    * Feedback mechanism should differentiate between seeming and actual
      relevance.
    * Relevant but inconclusive statements should get increasingly high scores
      as they are more helpful for answering the query.

    You can read more information about the performance of question statement
    relevance by viewing its [smoke test results](../qs_relevance_smoke_tests/).
    """
    # openai.relevance
    # openai.relevance_with_cot_reasons
    pass

class Groundedness(Semantics, WithPrompt):
    # hugs._summarized_groundedness
    # hugs._doc_groundedness

    prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template(
        """You are a INFORMATION OVERLAP classifier; providing the overlap of information between two statements.
Respond only as a number from 1 to 10 where 1 is no information overlap and 10 is all information is overlapping.
Never elaborate.

STATEMENT 1: {premise}

STATEMENT 2: {hypothesis}

INFORMATION OVERLAP: """)

class QuestionStatementRelevance(Relevance, WithPrompt):
    # openai.qs_relevance
    # openai.qs_relevance_with_cot_reasons

    prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template(
        """You are a RELEVANCE grader; providing the relevance of the given STATEMENT to the given QUESTION.
Respond only as a number from 1 to 10 where 1 is the least relevant and 10 is the most relevant. 

A few additional scoring guidelines:

- Long STATEMENTS should score equally well as short STATEMENTS.

- RELEVANCE score should increase as the STATEMENT provides more RELEVANT context to the QUESTION.

- RELEVANCE score should increase as the STATEMENT provides RELEVANT context to more parts of the QUESTION.

- STATEMENT that is RELEVANT to some of the QUESTION should score of 2, 3 or 4. Higher score indicates more RELEVANCE.

- STATEMENT that is RELEVANT to most of the QUESTION should get a score of 5, 6, 7 or 8. Higher score indicates more RELEVANCE.

- STATEMENT that is RELEVANT to the entire QUESTION should get a score of 9 or 10. Higher score indicates more RELEVANCE.

- STATEMENT must be relevant and helpful for answering the entire QUESTION to get a score of 10.

- Answers that intentionally do not answer the question, such as 'I don't know', should also be counted as the most relevant.

- Never elaborate.

QUESTION: {question}

STATEMENT: {statement}

RELEVANCE: """
    )


class Sentiment(Semantics):
    """
This evaluates the *positive sentiment* of either the prompt or response.

Sentiment is currently available to use with OpenAI, HuggingFace or Cohere as
the model provider.

* The OpenAI sentiment feedback function prompts a Chat Completion model to rate
  the sentiment from 1 to 10, and then scales the response down to 0-1.
* The HuggingFace sentiment feedback function returns a raw score from 0 to 1.
* The Cohere sentiment feedback function uses the classification endpoint and a
  small set of examples stored in `feedback_prompts.py` to return either a 0 or
  a 1.
    """
    # openai.sentiment
    # openai.sentiment_with_cot_reasons
    # hugs.positive_sentiment
    pass

class BinarySentiment(Sentiment, WithExamples):
    """
    A discrete form of sentiment with only "positive" (1) and "negative" (0) classification.
    """
    
    # cohere.sentiment

    # TODO: abstract examples type, make and move to BinarySentiment class
    examples: ClassVar[List[Example]] = [
        Example("The order came 5 days early", "1"),
        Example("I just got a promotion at work and I\'m so excited!", "1"),
        Example(
            "My best friend surprised me with tickets to my favorite band's concert.",
            "1"
        ),
        Example(
            "I\'m so grateful for my family's support during a difficult time.", "1"
        ),
        Example("It\'s kind of grungy, but the pumpkin pie slaps", "1"),
        Example(
            "I love spending time in nature and feeling connected to the earth.",
            "1"
        ),
        Example("I had an amazing meal at the new restaurant in town", "1"),
        Example("The pizza is good, but the staff is horrible to us", "0"),
        Example("The package was damaged", "0"),
        Example("I\'m feeling really sick and can\'t seem to shake it off", "0"),
        Example("I got into a car accident and my car is completely totaled.", "0"),
        Example(
            "My boss gave me a bad performance review and I might get fired", "0"
        ),
        Example("I got into a car accident and my car is completely totaled.", "0"),
        Example(
            "I\'m so disapointed in myself for not following through on my goals",
            "0"
        )
    ]

class Helpfulness(Semantics):
    # openai.helpfulness
    # openai.helpfulness_with_cot_reasons
    pass

class Controversiality(Semantics):
    # openai.controversiality
    # openai.controversiality_with_cot_reasons
    pass

class Moderation(Semantics):
    pass

class Legality(Semantics):
    pass

class Criminality(Legality): # maliciousness? harmfulness?
    # openai.criminality
    # openai.criminality_with_cot_reasons
    pass

class Harmfulness(Moderation):
    # openai.harmfulness
    # openai.harmfulness_with_cot_reasons
    pass

class Insensitivity(Semantics): # categorize
    # openai.insensitivity
    # openai.insensitivity_with_cot_reasons
    # hugs.not_toxic ?
    pass

class Toxicity(Semantics):
    # hugs.not_toxic
    pass

class Maliciousness(Moderation):
    # openai.maliciousness
    # openai.maliciousness_with_cot_reasons
    pass

class Disinofmration(Moderation, WithExamples):
    # cohere.not_disinformation

    # TODO: abstract examples type and reverse class
    examples: ClassVar[List[Example]] = [
        Example(
            "Bud Light Official SALES REPORT Just Released ′ 50% DROP In Sales ′ Total COLLAPSE ′ Bankruptcy?",
            "0"
        ),
        Example(
            "The Centers for Disease Control and Prevention quietly confirmed that at least 118,000 children and young adults have “died suddenly” in the U.S. since the COVID-19 vaccines rolled out,",
            "0"
        ),
        Example(
            "Silicon Valley Bank collapses, in biggest failure since financial crisis",
            "1"
        ),
        Example(
            "Biden admin says Alabama health officials didn’t address sewage system failures disproportionately affecting Black residents",
            "1"
        )
    ]
    
class Hate(Moderation):
    """
    TODO: docstring regarding hate, examples
    """
    # openai.moderation_not_hate

class Misogyny(Hate):
    # openai.misogyny
    # openai.misogyny_with_cot_reasons
    pass

class HateThreatening(Hate):
    """
    TODO: docstring regarding hate threatening, examples
    """
    # openai.not_hatethreatening

# others:
# OpenAI.moderation_not_selfharm
# OpenAI.moderation_not_sexual
# OpenAI.moderation_not_sexualminors
# OpenAI.moderation_not_violance
# OpenAI.moderation_not_violancegraphic

# Level 2 abstraction

## Feedback output types:

class FeedbackOutputType(pydantic.BaseModel):
    min_feedback: float
    max_feedback: float

    min_interpretation: Optional[str] = None
    max_interpretation: Optional[str] = None

class DigitalOutputType(FeedbackOutputType):
    min_feedback = 1.0
    max_feedback = 10.0
    
class BinaryOutputType(FeedbackOutputType):
    min_feedback = 0.0
    max_feedback = 1.0

class FeedbackOutput(pydantic.BaseModel):
    """
    Feedback functions produce at least a floating score.
    """
    feedback: float
    typ: FeedbackOutputType

class OutputWithExplanation(FeedbackOutput):
    reason: str

class Explained(Feedback):
    @staticmethod
    def of_feedback(feedback: WithPrompt):
        # Create the explained version of a feedback that is based on a prompt.
        pass

class OutputWithCOTExplanation(pydantic.BaseModel):
    reason: str
    reason_score: float

class COTExplanined(Feedback):
    COT_REASONS_TEMPLATE: str = \
    """
    Please answer with this template:

    TEMPLATE: 
    Supporting Evidence: <Give your reasons for scoring>
    Score: <The score 1-10 based on the given criteria>
    """

    # output_type: 

    @abstractmethod
    def extract_cot_explanation_of_response(self, response: str, normalize=10):
        pass

    @classmethod
    def of_feedback(cls, feedback: WithPrompt):
        # Create the cot explained version of a feedback that is based on a prompt.
        system_prompt = feedback.prompt

        system_prompt = system_prompt + cls.COT_REASONS_TEMPLATE

        class FeedbackWithExplanation(WithPrompt):
            prompt = system_prompt
            # TODO: things related to extracting score and reasons

            def extract_cot_explanation_of_response(self, response: str, normalize=10):
                if "Supporting Evidence" in response:
                    score = 0
                    for line in response.split('\n'):
                        if "Score" in line:
                            score = re_1_10_rating(line) / normalize
                    return score, {"reason": response}
                else:
                    return re_1_10_rating(response) / normalize

        return FeedbackWithExplanation(**feedback)

# Level 3 abstraction

class Model(pydantic.BaseModel):
    id: str

    # Which feedback function is this model for.
    feedback: Feedback

class CompletionModel(Model):
    
    max_output_tokens: int
    max_prompt_tokens: int

    @staticmethod
    def of_langchain_llm(llm):
        # Extract the model info from a langchain llm.
        pass

class ClassificationModel(Model):
    @staticmethod
    def of_prompt(model: CompletionModel, prompt: str, examples: Optional[List[Example]]):
        # OpenAI completion with examples
        # Cohere completion with examples

        # Cohere.sentiment
        # Cohere.not_disinformation

        """
        Define a classification model from a completion model, a prompt, and optional examples.
        """
        pass

class BinarySentimentModel(ClassificationModel):
    output_type = BinaryOutputType(min_interpretation="negative", max_interpretation="positive")

    # def classify()