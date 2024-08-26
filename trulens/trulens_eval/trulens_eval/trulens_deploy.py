from trulens_eval.tru_virtual import VirtualRecord
from trulens_eval import Select
from trulens_eval.feedback.provider.openai import AzureOpenAI
from trulens_eval.feedback.feedback import Feedback
from trulens_eval.tru_virtual import TruVirtual
#from trulens_eval.schema import Select
from trulens_eval.tru_virtual import VirtualApp
from trulens_eval import Tru
# tru = Tru(database_redact_keys=True)
# from trulens_eval.feedback import Groundedness

# from trulens.trulens_eval.trulens_eval.config import CONFIG
import os
import nltk
nltk.data.path.append("nltk/tokenize/")
# nltk.download('punkt')

# print("CONFIG : ", CONFIG["AZURE_OPENAI"]["gpt-3.5-turbo-16k"]["DEPLOYMENT_ID"])
print("CONFIG : ", os.environ.get("AZURE_API_BASE"))

def fill_virtual_records(data_dict, context_call):
    data = []
    for record in data_dict:
        rec = VirtualRecord(
            main_input=record['prompt'],
            main_output=record['response'],
            calls=
                {
                    context_call: dict(
                        args=[record['prompt']],
                        rets=[record['context']]
                    )
                }
            )
        data.append(rec)
    return data

def load_provider(dp_name, end_point, key_or_token, api_version):
    return AzureOpenAI(
                    deployment_name=dp_name, 
                    azure_endpoint=end_point,
                    azure_ad_token = key_or_token,
                    api_version=api_version
                )

def run_records(data_dict):
    retriever_component = Select.RecordCalls.retriever
    context_call = retriever_component.get_context
    data = fill_virtual_records(data_dict, context_call)

    # provider = load_provider(CONFIG["AZURE_OPENAI"]["gpt-3.5-turbo-16k"]["DEPLOYMENT_ID"], 
    #                           CONFIG["AZURE_OPENAI"]["AZURE_API_BASE"],
    #                           CONFIG["AZURE_OPENAI"]["AZURE_API_KEY"],
    #                           CONFIG["AZURE_OPENAI"]["AZURE_API_VERSION"]
    #                         )

    provider = load_provider(os.environ.get("AZURE_DEPLOYMENT_ID_GPT_35_TURBO_16K"), 
                              os.environ.get("AZURE_API_BASE"),
                              os.environ.get("AZURE_API_KEY"),
                              os.environ.get("AZURE_API_VERSION")
                            )

    context = context_call.rets[:]
    f_context_relevance = (Feedback(provider.qs_relevance, name = "Context Relevance")
            .on_input()
            .on(context)
    )
    # logger.info('Computing Groundedness')
    # grounded = Groundedness(groundedness_provider=provider)

    # Define a groundedness feedback function
    # f_groundedness = (
    #     Feedback(grounded.groundedness_measure_with_cot_reasons, name = "Groundedness")
    #              .on(context.collect())
    #              .on_output()
    #              .aggregate(grounded.grounded_statements_aggregator)
    # )



    # Question/answer relevance between overall question and answer.
    f_answer_relevance = (
        Feedback(provider.relevance_with_cot_reasons, name = "Answer Relevance")
        .on_input()
        .on(context)
    )

    virtual_app = dict(
        llm=dict(
            modelname="GPT 3.5"
        ),
        template="NA",
        debug="NA"
    )

    virtual_recorder = TruVirtual(
        app_id="ProfileHub1",
        app=virtual_app,
        feedbacks=[f_answer_relevance, f_context_relevance]
    )

    print(f"Number of records {len(data)}")
    for rec in data:
        virtual_recorder.add_record(rec)
        # print(f"processed {rec}")
        # logger.info(f'processed {rec}')
    virtual_app = VirtualApp(virtual_app)
    # print("Hello: ", context.collect())
    # logger.info(f'Hello: {context.collect()}')



















