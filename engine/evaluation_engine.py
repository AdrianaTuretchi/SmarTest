import re
from typing import List, Tuple

class EvaluationEngine:
    def __init__(self):
        pass

    def _extract_coordinates(self, answer: str) -> List[Tuple[int, int]]:
        """
        Extrage toate coordonatele de forma (r, c) dintr-un string.
        """
        pattern = r"\((\d+),\s*(\d+)\)"
        matches = re.findall(pattern, answer)
        return [(int(r), int(c)) for r, c in matches]

    def evaluate_nash_answer(self, user_answer: str, correct_coords: List[Tuple[int, int]]) -> float:
        """
        Compară răspunsul utilizatorului cu soluția corectă și returnează un scor între 0 și 1.
        """
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
