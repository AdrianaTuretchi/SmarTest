from typing import Any

from engine.evaluators import NashEvaluator, CSPEvaluator, MinMaxEvaluator


class EvaluationService:
    def __init__(self):
        # lazy instantiation (stateless) — create per request
        pass

    def evaluate(self, question_type: str, submission: Any) -> float:
        """
        Dispatch evaluation based on question_type.
        `submission` is expected to be a namespace/dict with fields required by the evaluator.
        Returns a float score.
        """
        if question_type == 'nash':
            evaluator = NashEvaluator()
            # submission should have 'user_answer' (str) and 'raw_data' (matrix)
            return evaluator.evaluate(submission.user_answer, submission.raw_data)

        if question_type == 'csp':
            evaluator = CSPEvaluator()
            return evaluator.evaluate(submission.user_answer, submission.raw_data)

        if question_type == 'minmax':
            evaluator = MinMaxEvaluator()
            # submission is expected to have root_value, visited_count and raw_data
            user_answer = {
                "root_value": submission.root_value,
                "visited_count": submission.visited_count,
            }
            return evaluator.evaluate(user_answer, submission.raw_data)

        raise ValueError(f"No evaluator for type '{question_type}'")
