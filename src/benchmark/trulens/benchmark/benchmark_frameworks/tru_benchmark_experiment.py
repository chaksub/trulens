from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import logging
from typing import Any, Callable, List, Optional, Tuple, Union

import pandas as pd
from pydantic import BaseModel
from trulens.core import Feedback
from trulens.core import Select
from trulens.core.app import TruCustomApp
from trulens.core.app.custom import instrument
from trulens.core.feedback.feedback import AggCallable
from trulens.core.utils.pyschema import FunctionOrMethod

log = logging.getLogger(__name__)


class BenchmarkParams(BaseModel):
    temperature: float = 0.0
    criteria: Optional[str] = None
    output_space: Optional[str] = None
    # TODO: support more parameters
    # "use_verb_confidence": False,
    # K should not be part of benchmark params b/c each set of benchmark params could have multiple set of K values for different metric aggregators


class TruBenchmarkExperiment:
    """
    Example usage:

    cortex = Cortex(model_engine="snowflake-arctic")

    def context_relevance_ff_to_score(input, output, temperature=0):
        return cortex.context_relevance(question=input, context=output, temperature=temperature)


    tru_labels = [1, 0, 0, ...] # ground truth labels collected from ground truth data collection
    mae_agg_func = GroundTruthAggregator(true_labels=true_labels).mae

    tru_benchmark_artic = tru.BenchmarkExperiment(
        app_id="MAE",
        feedback_fn=context_relevance_ff_to_score,
        agg_funcs=[mae_agg_func],
        benchmark_params=BenchmarkParams(temperature=0.5),
    )
    """

    def __init__(
        self,
        feedback_fn: Callable,
        agg_funcs: List[AggCallable],
        benchmark_params: BenchmarkParams,
    ):
        """Create a benchmark experiment class which defines custom
        feedback functions and aggregators to evaluate the feedback function on a ground truth dataset.
        Args:
            feedback_fn (Callable): function that takes in a row of ground truth data and returns a score by typically a LLM-as-judge
            agg_funcs (List[AggCallable]): list of aggregation functions to compute metrics on the feedback scores
            benchmark_params (BenchmarkParams): benchmark configuration parameters
        """

        self.feedback_fn = feedback_fn
        self.benchmark_params = benchmark_params

        self.f_benchmark_metrics: List[Feedback] = [
            Feedback(
                lambda x: x,
                name=f"metric_{agg_func.__name__}",
            )
            .on(Select.RecordCalls.run_score_generation_on_single_row.rets)
            .aggregate(agg_func)
            for agg_func in agg_funcs
        ]

    @instrument
    # def run_score_generation_on_single_row(
    #     self, row, feedback_fn: Callable
    # ) -> List[Union[float, Tuple[float, float]]]:
    #     """Generate a score with the feedback_fn

    #     Returns:
    #         List[Union[float, Tuple[float, Dict[str, float]]]]: feedback scores (with metadata) after running the benchmark on a single entry in ground truth data
    #     """

    #     benchmark_params_dict: dict = self.benchmark_params.model_dump()

    #     ret_lst = []
    #     if "expected_chunks" in row:
    #         for expected_chunk in row["expected_chunks"]:
    #             ret_lst.append(
    #                 feedback_fn(
    #                     row["query"],
    #                     expected_chunk["text"],
    #                     benchmark_params_dict,
    #                 )
    #             )
    #     elif "expected_response" in row:
    #         ret_lst.append(
    #             feedback_fn(
    #                 row["query"],
    #                 row["expected_response"],
    #                 benchmark_params_dict,
    #             )
    #         )

    #     for i in range(len(ret_lst)):
    #         if not isinstance(ret_lst[i], tuple) and not isinstance(
    #             ret_lst[i], float
    #         ):
    #             raise ValueError(
    #                 f"Output must be a float or a tuple, got {type(ret_lst[i])}"
    #             )

    #         if isinstance(ret_lst[i], tuple) and isinstance(
    #             ret_lst[i][1], dict
    #         ):
    #             ret_lst[i] = (
    #                 ret_lst[i][0],
    #                 list(ret_lst[i][1].values())[-1],
    #             )  # this is the case when a feedback function returns a tuple with a score and metadata like (0.5, {"confidence_score": 0.8})
    #     return ret_lst

    @instrument
    def run_score_generation_on_single_row(
        self,
        # row,
        feedback_fn: Callable,
        feedback_args: List[Any],
    ) -> Union[float, Tuple[float, float]]:
        """Generate a score with the feedback_fn

        Args:
            row: A single row from the dataset.
            feedback_fn: The function used to generate feedback scores.

        Returns:
            Union[float, Tuple[float, float]]: Feedback score (with metadata) after running the benchmark on a single entry in ground truth data.
        """

        benchmark_params_dict: dict = self.benchmark_params.model_dump()

        # Extract required values from the row based on the specified columns
        # feedback_args = [get_nested_value(row, col) for col in required_columns]

        # Append the benchmark parameters dictionary
        feedback_args.append(benchmark_params_dict)

        ret = feedback_fn(*feedback_args)

        if not isinstance(ret, tuple) and not isinstance(ret, float):
            raise ValueError(
                f"Output must be a float or a tuple, got {type(ret)}"
            )

        if isinstance(ret, tuple) and isinstance(ret[1], dict):
            ret = (
                ret[0],
                list(ret[1].values())[-1],
            )  # this is the case when a feedback function returns a tuple with a score and metadata like (0.5, {"confidence_score": 0.8})
        return ret

    @instrument
    def __call__(
        self,
        ground_truth: Union[
            List, Callable, pd.DataFrame, FunctionOrMethod
        ],  # TODO lock down type hints
    ) -> Union[
        List[float], List[Tuple[float]], Tuple[List[float], List[float]]
    ]:
        """Collect the list of generated feedback scores as input to the benchmark aggregation functions

        ground_truth (Union[List, Callable, pd.DataFrame, FunctionOrMethod]): ground truth dataset / collection to evaluate the feedback function on
        Returns:
            List[float]: feedback scores after running the benchmark on all entries in ground truth data
        """

        # TODO: instance type check of ground_truth argument + handle groundtruth_impl

        scores = []
        meta_scores = []
        with ThreadPoolExecutor() as executor:
            future_to_index = {}  # Map each future to the index of the row
            index_to_results = {}  # Store results based on the original index

            # Submit tasks to the executor
            for index, row in ground_truth.iterrows():
                if "expected_chunks" in row:
                    for expected_chunk in row["expected_chunks"]:
                        future = executor.submit(
                            self.run_score_generation_on_single_row,
                            self.feedback_fn,
                            [row["query"], expected_chunk["text"]],
                        )
                        future_to_index[future] = index
                elif "expected_response" in row:
                    future = executor.submit(
                        self.run_score_generation_on_single_row,
                        self.feedback_fn,
                        [row["query"], row["expected_response"]],
                    )
                    future_to_index[future] = index

            # Process futures as they complete
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    ret_lst = future.result()
                    index_to_results.setdefault(index, []).extend(ret_lst)

                except Exception as e:
                    log.error(f"Row generated an exception: {e}")

            # Process results in the original order
            for index in range(len(ground_truth)):
                if index in index_to_results:
                    ret_lst = index_to_results[index]
                    for ret in ret_lst:
                        if isinstance(ret, float):
                            score = ret
                        else:
                            score, metadata = ret
                            meta_scores.append(metadata)

                        scores.append(score)

        if meta_scores:
            return scores, meta_scores
        else:
            return scores


@staticmethod
def create_benchmark_experiment_app(
    app_id: str, benchmark_experiment: TruBenchmarkExperiment, **kwargs
) -> TruCustomApp:
    """Create a Custom app for special use case: benchmarking feedback functions.

    Args:
        app_id (str): user-defined identifier of the experiment run.
        feedback_fn (Callable): feedback function of interest to perform meta-evaluation on.
        agg_funcs (List[feedback.AggCallable]): list of aggregation functions to compute metrics for the benchmark.
        benchmark_params (Any): parameters for the benchmarking experiment.

    Returns:
        trulens.core.app.TruCustomApp: Custom app wrapper for benchmarking feedback functions.
    """

    return TruCustomApp(
        benchmark_experiment,
        app_id=app_id,
        feedbacks=benchmark_experiment.f_benchmark_metrics,
        **kwargs,
    )
