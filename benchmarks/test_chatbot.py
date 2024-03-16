import pytest
from deepeval import assert_test
from deepeval.metrics import GEval, AnswerRelevancyMetric, BaseMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


def test_case():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    test_case = LLMTestCase(
        input="What if these shoes don't fit?",
        # Replace this with the actual output from your LLM application
        actual_output="Try getting a bigger size",
        retrieval_context=[
            "All customers are eligible for a 30 day full refund at no extra costs."
        ],
    )
    assert_test(test_case, [answer_relevancy_metric])


def test_coherence():
    coherence_metric = GEval(
        name="Coherence",
        criteria="Coherence - determine if the actual output is logical, has flow, and is easy to understand and follow.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.5,
    )
    test_case = LLMTestCase(
        input="What if these shoes don't fit? I want a full refund.",
        # Replace this with the actual output from your LLM application
        actual_output="If the shoes don't fit, the customer wants a full refund.",
    )
    assert_test(test_case, [coherence_metric])


# class LengthMetric(BaseMetric):
#     # This metric checks if the output length is greater than 10 characters
#     def __init__(self, max_length: int = 10):
#         self.threshold = max_length

#     def measure(self, test_case: LLMTestCase):
#         self.success = len(test_case.actual_output) > self.threshold
#         if self.success:
#             score = 1
#         else:
#             score = 0
#         return score

#     def is_successful(self):
#         return self.success

#     @property
#     def __name__(self):
#         return "Length"


# def test_length():
#     length_metric = LengthMetric(max_length=10)
#     test_case = LLMTestCase(
#         input="What if these shoes don't fit?",
#         # Replace this with the actual output of your LLM application
#         actual_output="We offer a 30-day full refund at no extra cost.",
#     )
#     assert_test(test_case, [length_metric])
