import re
from typing import List, Tuple
from core_logic.nash_logic import find_pure_nash


class NashEvaluator:
    def __init__(self):
        pass

    def _extract_coordinates(self, answer: str) -> List[Tuple[int, int]]:
        pattern = r"\((\d+),\s*(\d+)\)"
        matches = re.findall(pattern, answer)
        return [(int(r), int(c)) for r, c in matches]

    def evaluate(self, user_answer: str, raw_data: List[List[Tuple[int, int]]]) -> float:
        """
        Evaluate a Nash-style answer. Returns float score between 0 and 1.
        """
        correct_coords = find_pure_nash(raw_data)
        user_coords = self._extract_coordinates(user_answer)

        if not user_coords:
            return 0.0

        correct_set = set(correct_coords)
        user_set = set(user_coords)

        if not correct_set:
            return 1.0 if not user_set else 0.0

        intersection = correct_set.intersection(user_set)
        score = len(intersection) / len(correct_set)
        return score
