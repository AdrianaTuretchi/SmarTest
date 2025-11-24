from typing import Dict, Any
from core_logic.minmax_logic import dict_to_tree, minmax


class MinMaxEvaluator:
    def __init__(self):
        pass

    def evaluate(self, user_answer: Dict[str, Any], raw_data: Dict[str, Any]) -> float:
        """Evaluate a user's MinMax answer.

        user_answer: {"root_value": int, "visited_count": int}
        raw_data: dict representation of the tree
        Returns a float score between 0.0 and 1.0
        """
        # Reconstruct tree and compute correct values
        tree = dict_to_tree(raw_data)
        visited = []
        try:
            correct_root = minmax(tree, 0, float('-inf'), float('inf'), True, visited)
            correct_visited = len(visited)
        except Exception:
            return 0.0

        # Extract user's values
        try:
            user_root = int(user_answer.get("root_value"))
            user_visited = int(user_answer.get("visited_count"))
        except Exception:
            return 0.0

        # Strict scoring: both correct -> 1.0
        if user_root == correct_root and user_visited == correct_visited:
            return 1.0

        # Partial scoring: 70% for correct root, 30% for correct visited count
        score = 0.0
        if user_root == correct_root:
            score += 0.7
        if user_visited == correct_visited:
            score += 0.3

        return round(score, 3)
