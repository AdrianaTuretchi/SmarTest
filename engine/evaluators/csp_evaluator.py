from typing import Dict, Any, Optional, Tuple
from core_logic.csp_logic import backtrack, ac3


class CSPEvaluator:
    def __init__(self):
        pass

    def evaluate(self, user_answer: Dict[str, int], raw_data: Dict[str, Any], has_solution: Optional[bool] = None) -> Tuple[float, Optional[Dict[str, int]], bool, str]:
        """
        Evaluate CSP submission.
        
        Returns:
            Tuple of (score, correct_assignment, problem_has_solution, feedback)
        """
        try:
            variables = raw_data['variables']
            domains = raw_data['domains']
            constraints = raw_data['constraints']
            partial_assignment = raw_data.get('partial_assignment', {})
            tags = raw_data.get('tags', [])
        except Exception:
            return 0.0, None, False, "Date invalide în întrebare"

        # Determine solving method based on tags
        # Aplicăm partial assignment la domenii pentru AC-3
        domains_for_ac3 = {k: list(v) for k, v in domains.items()}
        for var, val in partial_assignment.items():
            if var in domains_for_ac3:
                domains_for_ac3[var] = [val]

        try:
            if 'use_ac3' in tags:
                # Use AC-3 for arc consistency, then backtracking
                reduced_domains = ac3(variables, domains_for_ac3, [(c[0], c[1]) for c in constraints])
                if reduced_domains is not None:
                    # AC-3 succeeded, use backtracking on reduced domains
                    correct_solution = backtrack(
                        variables, 
                        reduced_domains, 
                        [(c[0], c[1]) for c in constraints], 
                        partial_assignment
                    )
                else:
                    correct_solution = None
            else:
                # Use Backtracking with optional MRV and Forward Checking
                use_mrv = 'use_mrv' in tags
                use_fc = 'use_forward_checking' in tags
                correct_solution = backtrack(
                    variables, 
                    domains, 
                    [(c[0], c[1]) for c in constraints], 
                    partial_assignment, 
                    use_mrv, 
                    use_fc
                )
        except Exception as e:
            correct_solution = None

        problem_has_solution = correct_solution is not None

        # Evaluăm răspunsul utilizatorului
        score = 0.0
        feedback = ""

        # Dacă utilizatorul a răspuns la întrebarea "are soluție?"
        if has_solution is not None:
            if has_solution == problem_has_solution:
                # A răspuns corect la "are soluție?"
                if not problem_has_solution:
                    # Problema nu are soluție și utilizatorul a zis corect
                    score = 1.0
                    feedback = "Corect! Problema nu are soluție - constrângerile sunt inconsistente."
                else:
                    # Problema are soluție, verificăm și asignarea
                    try:
                        user_normalized = {str(k): int(v) for k, v in user_answer.items()}
                    except Exception:
                        user_normalized = {}

                    merged = dict(partial_assignment)
                    merged.update(user_normalized)

                    if merged == correct_solution:
                        score = 1.0
                        feedback = "Corect! Soluția este validă."
                    else:
                        # Verificăm dacă soluția utilizatorului este validă (poate fi o altă soluție)
                        if self._is_valid_solution(merged, variables, domains, constraints):
                            score = 1.0
                            feedback = "Corect! Soluția ta este validă (poate diferi de soluția noastră)."
                        else:
                            score = 0.5  # Parțial - a zis că are soluție dar a dat soluție greșită
                            feedback = "Ai identificat corect că problema are soluție, dar asignarea nu este validă."
            else:
                # A răspuns greșit la "are soluție?"
                score = 0.0
                if problem_has_solution:
                    feedback = "Incorect. Problema ARE soluție."
                else:
                    feedback = "Incorect. Problema NU are soluție - constrângerile sunt inconsistente."
        else:
            # Vechea logică pentru compatibilitate (fără has_solution)
            if correct_solution is None:
                score = 1.0 if not user_answer else 0.0
                feedback = "Problema nu are soluție." if not user_answer else "Problema nu are soluție, dar ai dat o asignare."
            else:
                try:
                    user_normalized = {str(k): int(v) for k, v in user_answer.items()}
                except Exception:
                    return 0.0, correct_solution, True, "Răspuns invalid"

                merged = dict(partial_assignment)
                merged.update(user_normalized)

                if merged == correct_solution:
                    score = 1.0
                    feedback = "Corect!"
                elif self._is_valid_solution(merged, variables, domains, constraints):
                    score = 1.0
                    feedback = "Corect! Soluția ta este validă."
                else:
                    score = 0.0
                    feedback = "Soluția nu satisface toate constrângerile."

        return score, correct_solution, problem_has_solution, feedback

    def _is_valid_solution(self, assignment: Dict[str, int], variables: list, domains: dict, constraints: list) -> bool:
        """
        Verifică dacă o asignare este validă pentru CSP.
        """
        # Verificăm că toate variabilele sunt asignate
        for v in variables:
            if v not in assignment:
                return False
            # Verificăm că valoarea este în domeniu
            if assignment[v] not in domains.get(v, []):
                return False

        # Verificăm constrângerile (toate sunt !=)
        for c in constraints:
            if len(c) >= 2:
                v1, v2 = c[0], c[1]
                if v1 in assignment and v2 in assignment:
                    if assignment[v1] == assignment[v2]:
                        return False

        return True
