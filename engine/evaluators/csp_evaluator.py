from typing import Dict, Any
from core_logic.csp_logic import backtrack


class CSPEvaluator:
    def __init__(self):
        pass

    def evaluate(self, user_answer: Dict[str, int], raw_data: Dict[str, Any]) -> float:
        """
        Evaluate CSP submission: return 1.0 if user's assignment (merged with partial)
        matches the backtrack solution; otherwise 0.0.
        """
        try:
            variables = raw_data['variables']
            domains = raw_data['domains']
            constraints = raw_data['constraints']
            partial_assignment = raw_data.get('partial_assignment', {})
        except Exception:
            return 0.0

        correct = backtrack(variables, domains, constraints, partial_assignment)

        if correct is None:
            return 1.0 if not user_answer else 0.0

        try:
            user_normalized = {str(k): int(v) for k, v in user_answer.items()}
        except Exception:
            return 0.0

        merged = dict(partial_assignment)
        merged.update(user_normalized)

        return 1.0 if merged == correct else 0.0
