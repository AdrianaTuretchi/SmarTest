import random
from typing import List, Tuple, Dict, Any

Matrix = List[List[Tuple[int, int]]]


class NashGenerator:
    def __init__(self, templates: Dict[str, Dict[str, Any]]):
        # templates: mapping id -> template dict
        self.templates = templates or {}

    def _generate_nash_data(self) -> Matrix:
        rows = random.randint(2, 3)
        cols = random.randint(2, 3)

        matrix = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                p1_payoff = random.randint(0, 9)
                p2_payoff = random.randint(0, 9)
                row.append((p1_payoff, p2_payoff))
            matrix.append(row)

        return matrix

    def _format_matrix_as_string(self, matrix: Matrix) -> str:
        matrix_str = "\nMatricea de plăți (Jucător 1: rânduri, Jucător 2: coloane):\n"
        matrix_str += "--------------------------------------------------\n"

        for row in matrix:
            row_str = "\t".join([f"({p1},{p2})" for p1, p2 in row])
            matrix_str += f"\t{row_str}\n"

        matrix_str += "--------------------------------------------------\n"
        return matrix_str

    def generate(self) -> Dict[str, Any]:
        if not self.templates:
            return {"error": "Nu s-au găsit șabloane pentru tipul 'nash'."}

        template_id = random.choice(list(self.templates.keys()))
        template_text = self.templates[template_id]['template']

        raw_matrix = self._generate_nash_data()
        formatted_matrix_str = self._format_matrix_as_string(raw_matrix)
        final_question_text = template_text + "\n" + formatted_matrix_str

        return {
            "question_text": final_question_text,
            "raw_data": raw_matrix,
            "template_id": template_id,
        }
