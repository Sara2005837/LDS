from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric


test_case = LLMTestCase(
    input="What did the researchers develop and validate?",
    actual_output="The researchers developed and validated a scale for dependence on artificial intelligence among university students.",
    retrieval_context=[
        "The objective of this study was to develop and validate a scale to measure dependence on artificial intelligence among university students."
    ],
)


metric = AnswerRelevancyMetric(
    threshold=0.5,
    model="llama3",
)

evaluate(
    [test_case],
    [metric],
)
