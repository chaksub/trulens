from typing import List
from pydantic import BaseModel
import streamlit as st
from streamlit_pills import pills

from trulens_eval.schema.record import Record
from trulens_eval.schema.feedback import FeedbackCall
from trulens_eval.schema.feedback import FeedbackDefinition
from trulens_eval.utils import display
from trulens_eval.utils.python import Future
from trulens_eval.ux.styles import CATEGORY


class FeedbackDisplay(BaseModel):
    score: float = 0
    calls: List[FeedbackCall]
    icon: str


@st.experimental_fragment(run_every=2)
def trulens_feedback(record: Record):
    feedback_cols = []
    feedbacks = {}
    icons = []
    for feedback, feedback_result in record.wait_for_feedback_results().items():
        print(feedback.name, feedback_result.result)
        call_data = {
            'feedback_definition': feedback,
            'feedback_name': feedback.name,
            'result': feedback_result.result
        }
        feedback_cols.append(call_data['feedback_name'])
        feedbacks[call_data['feedback_name']] = FeedbackDisplay(
            score=call_data['result'],
            calls=[],
            icon=_get_icon(fdef=feedback, result=feedback_result.result)
        )
        icons.append(feedbacks[call_data['feedback_name']].icon)

    st.write('**Feedback functions**')
    selected_feedback = pills(
        "Feedback functions",
        feedback_cols,
        index=None,
        format_func=lambda fcol: f"{fcol} {feedbacks[fcol].score:.4f}",
        label_visibility=
        "collapsed",  # Hiding because we can't format the label here.
        icons=icons,
        key=
        f"{call_data['feedback_name']}_{len(feedbacks)}"  # Important! Otherwise streamlit sometimes lazily skips update even with st.exprimental_fragment
    )

    if selected_feedback is not None:
        st.dataframe(
            display.get_feedback_result(
                record, feedback_name=selected_feedback
            ),
            use_container_width=True,
            hide_index=True
        )


def _get_icon(fdef: FeedbackDefinition, result: float):
    cat = CATEGORY.of_score(
        result or 0,
        higher_is_better=fdef.higher_is_better
        if fdef.higher_is_better is not None else True
    )
    return cat.icon