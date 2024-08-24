"""
Tests server-side feedback evaluations in Snowflake.
"""

import time
from unittest import main

from trulens.core import Feedback
from trulens.core import SnowflakeFeedback
from trulens.core import TruBasicApp
from trulens.core import TruSession
from trulens.core.schema.feedback import FeedbackMode
from trulens.core.schema.feedback import FeedbackRunLocation
from trulens.providers.cortex.provider import Cortex
from trulens.providers.openai.provider import OpenAI

from tests.test import optional_test
from tests.util.snowflake_test_case import SnowflakeTestCase


def silly_feedback_function(q: str) -> float:
    return 0.1


class TestSnowflakeFeedbackEvaluation(SnowflakeTestCase):
    def _suspend_task(self) -> None:
        self._snowflake_session.sql(
            f"ALTER TASK {self._database_name}.{self._schema_name}.TRULENS_FEEDBACK_EVAL_TASK SUSPEND"
        ).collect()

    def _wait_till_feedbacks_done(
        self, num_expected_feedbacks: int, timeout_in_seconds: int = 120
    ):
        start_time = time.time()
        while time.time() - start_time < timeout_in_seconds:
            res = self._snowflake_session.sql(
                f"SELECT STATUS FROM {self._database_name}.{self._schema_name}.TRULENS_FEEDBACKS"
            ).collect()
            if len(res) == num_expected_feedbacks and all([
                curr.STATUS == "done" for curr in res
            ]):
                break
            time.sleep(1)

    @optional_test
    def test_local_deferred_mode(self) -> None:
        session = TruSession()
        session.reset_database()
        f = Feedback(silly_feedback_function).on_default()
        tru_app = TruBasicApp(
            text_to_text=lambda t: f"returning {t}",
            feedbacks=[f],
            feedback_mode=FeedbackMode.DEFERRED,
        )
        with tru_app:
            tru_app.main_call("test_local_deferred_mode")
        time.sleep(2)
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertEqual(len(records_and_feedback[1]), 0)
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        session.start_evaluator()
        time.sleep(2)
        session.stop_evaluator()
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertEqual(records_and_feedback[1], ["silly_feedback_function"])
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertEqual(
            records_and_feedback[0]["silly_feedback_function"].iloc[0],
            0.1,
        )

    @optional_test
    def test_snowflake_deferred_mode(self) -> None:
        session = self.get_session("test_snowflake_deferred_mode")
        self._suspend_task()
        f_local = Feedback(silly_feedback_function).on_default()
        f_snowflake = SnowflakeFeedback(Cortex().relevance).on_input_output()
        tru_app = TruBasicApp(
            text_to_text=lambda _: "Tokyo is the capital of Japan.",
            feedbacks=[f_local, f_snowflake],
            feedback_mode=FeedbackMode.DEFERRED,
        )
        with tru_app:
            tru_app.main_call("What is the capital of Japan?")
        time.sleep(2)
        session.start_evaluator()
        time.sleep(2)
        session.stop_evaluator()
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertEqual(records_and_feedback[1], ["silly_feedback_function"])
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertEqual(
            records_and_feedback[0]["silly_feedback_function"].iloc[0],
            0.1,
        )
        session.start_evaluator(run_location=FeedbackRunLocation.SNOWFLAKE)
        time.sleep(2)
        session.stop_evaluator()
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertListEqual(
            sorted(records_and_feedback[1]),
            ["relevance", "silly_feedback_function"],
        )
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertEqual(
            records_and_feedback[0]["silly_feedback_function"].iloc[0],
            0.1,
        )
        self.assertGreaterEqual(
            records_and_feedback[0]["relevance"].iloc[0],
            0.8,
        )

    @optional_test
    def test_snowflake_feedback_is_always_deferred(self) -> None:
        session = self.get_session("test_snowflake_feedback_is_always_deferred")
        self._suspend_task()
        f_local = Feedback(silly_feedback_function).on_default()
        f_snowflake = SnowflakeFeedback(Cortex().relevance).on_input_output()
        tru_app = TruBasicApp(
            text_to_text=lambda _: "Tokyo is the capital of Japan.",
            feedbacks=[f_local, f_snowflake],
        )
        with tru_app:
            tru_app.main_call("What is the capital of Japan?")
        time.sleep(2)
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertEqual(records_and_feedback[1], ["silly_feedback_function"])
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertEqual(
            records_and_feedback[0]["silly_feedback_function"].iloc[0],
            0.1,
        )
        session.start_evaluator(run_location=FeedbackRunLocation.SNOWFLAKE)
        time.sleep(2)
        session.stop_evaluator()
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertListEqual(
            sorted(records_and_feedback[1]),
            ["relevance", "silly_feedback_function"],
        )
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertEqual(
            records_and_feedback[0]["silly_feedback_function"].iloc[0],
            0.1,
        )
        self.assertGreaterEqual(
            records_and_feedback[0]["relevance"].iloc[0],
            0.8,
        )

    @optional_test
    def test_snowflake_feedback_setup(self) -> None:
        self.get_session("test_snowflake_feedback_setup")
        TruBasicApp(
            text_to_text=lambda t: f"returning {t}",
        )
        # Test stage exists.
        res = self._snowflake_session.sql(
            f"SHOW TERSE STAGES IN SCHEMA {self._database_name}.{self._schema_name}"
        ).collect()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "TRULENS_PACKAGES_STAGE")
        self.assertEqual(res[0].database_name, self._database_name.upper())
        self.assertEqual(res[0].schema_name, self._schema_name.upper())
        # Test stream exists.
        res = self._snowflake_session.sql(
            f"SHOW TERSE STREAMS IN SCHEMA {self._database_name}.{self._schema_name}"
        ).collect()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "TRULENS_FEEDBACK_EVALS_STREAM")
        self.assertEqual(res[0].database_name, self._database_name.upper())
        self.assertEqual(res[0].schema_name, self._schema_name.upper())
        self.assertEqual(res[0].tableOn, "TRULENS_FEEDBACKS")
        # Test stored procedure exists.
        res = self._snowflake_session.sql(
            f"SHOW TERSE PROCEDURES LIKE 'TRULENS_RUN_DEFERRED_FEEDBACKS' IN SCHEMA {self._database_name}.{self._schema_name}"
        ).collect()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "TRULENS_RUN_DEFERRED_FEEDBACKS")
        self.assertEqual(res[0].schema_name, self._schema_name.upper())
        # Test task exists.
        res = self._snowflake_session.sql(
            f"SHOW TERSE TASKS IN SCHEMA {self._database_name}.{self._schema_name}"
        ).collect()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "TRULENS_FEEDBACK_EVAL_TASK")
        self.assertEqual(res[0].database_name, self._database_name.upper())
        self.assertEqual(res[0].schema_name, self._schema_name.upper())

    @optional_test
    def test_snowflake_feedback_ran(self) -> None:
        session = self.get_session("test_snowflake_feedback_ran")
        f_snowflake = SnowflakeFeedback(Cortex().relevance).on_input_output()
        tru_app = TruBasicApp(
            text_to_text=lambda _: "Tokyo is the capital of Japan.",
            feedbacks=[f_snowflake],
        )
        with tru_app:
            tru_app.main_call("What is the capital of Japan?")
        self._wait_till_feedbacks_done(num_expected_feedbacks=1)
        records_and_feedback = session.get_records_and_feedback()
        self.assertEqual(len(records_and_feedback), 2)
        self.assertListEqual(
            records_and_feedback[1],
            ["relevance"],
        )
        self.assertEqual(records_and_feedback[0].shape[0], 1)
        self.assertGreaterEqual(
            records_and_feedback[0]["relevance"].iloc[0],
            0.8,
        )

    @optional_test
    def test_snowflake_feedback_only_runs_cortex(self) -> None:
        SnowflakeFeedback(Cortex().relevance)  # no error
        with self.assertRaisesRegex(
            ValueError,
            "`SnowflakeFeedback` can only support feedback functions defined in `trulens-providers-cortex` package's, `trulens.providers.cortex.provider.Cortex` class!",
        ):
            SnowflakeFeedback(OpenAI().relevance)


if __name__ == "__main__":
    main()
