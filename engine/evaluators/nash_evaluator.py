import re
from typing import List, Tuple, Dict, Optional
from core_logic.nash_logic import find_pure_nash, find_dominated_strategies


class NashEvaluator:
    def __init__(self):
        pass

    def _extract_coordinates(self, answer: str) -> List[Tuple[int, int]]:
        if not answer:
            return []
        pattern = r"\((\d+),\s*(\d+)\)"
        matches = re.findall(pattern, str(answer))
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

    def evaluate_extended(
        self, 
        raw_data: List[List[Tuple[int, int]]],
        user_answer: str,
        has_dominated: Optional[bool] = None,
        dominated_p1: Optional[List[int]] = None,
        dominated_p2: Optional[List[int]] = None,
        has_equilibrium: Optional[bool] = None
    ) -> Tuple[float, Dict]:
        """
        Evaluează un răspuns extins care include și strategii dominate.
        
        Returns:
            Tuple[float, Dict]: (scor_total, detalii_evaluare)
        """
        # Calculăm răspunsurile corecte
        correct_coords = find_pure_nash(raw_data)
        correct_dominated = find_dominated_strategies(raw_data)
        
        has_correct_dominated = bool(correct_dominated['player1'] or correct_dominated['player2'])
        has_correct_equilibrium = bool(correct_coords)
        
        scores = {}
        total_points = 0
        earned_points = 0
        
        # Evaluăm partea despre strategii dominate (dacă a fost răspuns)
        if has_dominated is not None:
            total_points += 1  # 1 punct pentru răspunsul da/nu
            
            if has_dominated == has_correct_dominated:
                earned_points += 1
                scores['dominated_existence'] = 1.0
            else:
                scores['dominated_existence'] = 0.0
            
            # Dacă a zis că există, verificăm dacă le-a identificat corect
            if has_dominated and (dominated_p1 is not None or dominated_p2 is not None):
                total_points += 1  # 1 punct pentru identificarea strategiilor
                
                user_p1 = set(dominated_p1 or [])
                user_p2 = set(dominated_p2 or [])
                correct_p1 = set(correct_dominated['player1'])
                correct_p2 = set(correct_dominated['player2'])
                
                # Calculăm acuratețea
                all_correct = correct_p1.union(correct_p2)
                all_user = user_p1.union(user_p2)
                
                if all_correct:
                    intersection = len(all_correct.intersection(all_user))
                    false_positives = len(all_user - all_correct)
                    dom_score = max(0, (intersection - false_positives * 0.5) / len(all_correct))
                    scores['dominated_identification'] = min(1.0, dom_score)
                    earned_points += scores['dominated_identification']
                else:
                    # Nu există strategii dominate, dar utilizatorul a dat unele
                    scores['dominated_identification'] = 0.0 if all_user else 1.0
                    earned_points += scores['dominated_identification']
        
        # Evaluăm partea despre echilibru Nash
        if has_equilibrium is not None:
            total_points += 1  # 1 punct pentru răspunsul da/nu
            
            if has_equilibrium == has_correct_equilibrium:
                earned_points += 1
                scores['equilibrium_existence'] = 1.0
            else:
                scores['equilibrium_existence'] = 0.0
        
        # Evaluăm coordonatele echilibrului (întotdeauna, dacă user_answer nu e gol)
        if user_answer and user_answer.strip():
            total_points += 1  # 1 punct pentru identificarea echilibrului
            
            user_coords = self._extract_coordinates(user_answer)
            correct_set = set(correct_coords)
            user_set = set(user_coords)
            
            if not correct_set:
                # Nu există echilibre - scor 1 dacă utilizatorul nu a dat nimic, 0 altfel
                if not user_set:
                    scores['equilibrium_coords'] = 1.0
                else:
                    scores['equilibrium_coords'] = 0.0
            else:
                intersection = correct_set.intersection(user_set)
                false_positives = len(user_set - correct_set)
                eq_score = max(0, (len(intersection) - false_positives * 0.5) / len(correct_set))
                scores['equilibrium_coords'] = min(1.0, eq_score)
            
            earned_points += scores['equilibrium_coords']
        
        # Calculăm scorul final
        final_score = earned_points / total_points if total_points > 0 else 0.0
        
        details = {
            'scores': scores,
            'correct_dominated': correct_dominated,
            'correct_coords': correct_coords,
            'has_correct_dominated': has_correct_dominated,
            'has_correct_equilibrium': has_correct_equilibrium
        }
        
        return final_score, details
