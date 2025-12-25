from typing import Dict, Any
from core_logic.csp_logic import backtrack, ac3


class CSPEvaluator:
    def __init__(self):
        pass

    def evaluate(self, user_answer: Dict[str, int], raw_data: Dict[str, Any]) -> float:
        """
        Evaluate CSP submission: return 1.0 if user's assignment (merged with partial)
        matches the solution determined by the appropriate algorithm based on tags; otherwise 0.0.
        """
        try:
            variables = raw_data['variables']
            domains = raw_data['domains']
            constraints = raw_data['constraints']
            partial_assignment = raw_data.get('partial_assignment', {})
            tags = raw_data.get('tags', [])
        except Exception:
            return 0.0

        # Determine solving method based on tags
        try:
            if 'use_ac3' in tags:
                # Use AC-3 for arc consistency
                correct_solution = ac3(variables, domains, constraints)
                correct_solution = correct_solution if correct_solution else None
            else:
                # Use Backtracking with optional MRV and Forward Checking
                use_mrv = 'use_mrv' in tags
                use_fc = 'use_forward_checking' in tags
                correct_solution = backtrack(variables, domains, constraints, partial_assignment, use_mrv, use_fc)
        except Exception:
            correct_solution = None

        if correct_solution is None:
            return 1.0 if not user_answer else 0.0

        try:
            user_normalized = {str(k): int(v) for k, v in user_answer.items()}
        except Exception:
            return 0.0

        merged = dict(partial_assignment)
        merged.update(user_normalized)

        return 1.0 if merged == correct_solution else 0.0
