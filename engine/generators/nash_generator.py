import random
from typing import List, Tuple, Dict, Any, Optional

Matrix = List[List[Tuple[int, int]]]


class NashGenerator:
    # Tags that trigger data generation
    DATA_TRIGGER_TAGS = {'requires_calculation', 'hybrid'}
    
    def __init__(self, templates: Dict[str, Dict[str, Any]]):
        # templates: mapping id -> template dict
        # Filter only Nash templates (those with 'nash' in tags)
        self.nash_templates = {
            tid: tmpl for tid, tmpl in (templates or {}).items()
            if 'nash' in tmpl.get('tags', [])
        }

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
        matrix_str = "\nMatricea de plati (Jucator 1: randuri, Jucator 2: coloane):\n"
        matrix_str += "--------------------------------------------------\n"

        for row in matrix:
            row_str = "\t".join([f"({p1},{p2})" for p1, p2 in row])
            matrix_str += f"\t{row_str}\n"

        matrix_str += "--------------------------------------------------\n"
        return matrix_str

    def generate(self) -> Dict[str, Any]:
        if not self.nash_templates:
            return {"error": "Nu s-au găsit șabloane pentru tipul 'nash'."}

        # Select template
        template_id = random.choice(list(self.nash_templates.keys()))
        selected_template = self.nash_templates[template_id]
        template_text = selected_template['template']
        template_tags = set(selected_template.get('tags', []))
        
        # Check if data generation is needed
        needs_data = bool(template_tags & self.DATA_TRIGGER_TAGS)
        
        # Check if template requires dominated strategies analysis
        requires_dominated = 'dominated-strategies' in template_tags
        
        if needs_data:
            # Generate and append data for calculation-based questions
            raw_matrix = self._generate_nash_data()
            formatted_matrix_str = self._format_matrix_as_string(raw_matrix)
            final_question_text = template_text + "\n" + formatted_matrix_str
            raw_data = raw_matrix
        else:
            # Pure theory question - no data generation
            final_question_text = template_text
            raw_data = None

        return {
            "question_text": final_question_text,
            "raw_data": raw_data,
            "template_id": template_id,
            "requires_dominated": requires_dominated,
        }
