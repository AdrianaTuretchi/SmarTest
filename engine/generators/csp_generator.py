from typing import List, Tuple, Dict, Any


class CSPGenerator:
    def __init__(self):
        pass

    def _generate_csp_data(self):
        variables = ['A', 'B', 'C']
        domains = {v: [1, 2, 3] for v in variables}
        constraints = [('A', 'B'), ('B', 'C')]
        partial_assignment = {'A': 1}
        return variables, domains, constraints, partial_assignment

    def _format_csp_string(self, data) -> str:
        variables, domains, constraints, partial_assignment = data
        question_text = (
            "Avem următoarea instanță CSP:\n"
            f"Variabile: {variables}\n"
            f"Domenii: {domains}\n"
            f"Constrângeri: A ≠ B, B ≠ C\n"
            f"Asigare parțială: {partial_assignment}\n\n"
            "Care va fi asignarea variabilelor rămase dacă folosim Backtracking cu optimizarea Forward Checking și MRV?"
        )
        return question_text

    def generate(self) -> Dict[str, Any]:
        data = self._generate_csp_data()
        question_text = self._format_csp_string(data)
        variables, domains, constraints, partial_assignment = data
        raw_data = {
            'variables': variables,
            'domains': domains,
            'constraints': constraints,
            'partial_assignment': partial_assignment,
        }
        return {
            'question_text': question_text,
            'raw_data': raw_data,
            'template_id': 'csp-default',
        }
