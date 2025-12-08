"""
Answer Generator Module
Combines mathematical results with theoretical justifications from the knowledge base.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class AnswerGenerator:
    """
    Generates comprehensive answers that combine calculated results
    with theoretical explanations from the knowledge base.
    """
    
    def __init__(self, knowledge_base_path: str):
        """
        Initialize the answer generator and load the knowledge base.
        
        Args:
            knowledge_base_path: Path to the knowledge_base.json file
        """
        self.knowledge_base = []
        
        try:
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load knowledge base from {knowledge_base_path}: {e}")
            self.knowledge_base = []
    
    def _format_math_result(self, q_type: str, result: Any) -> str:
        """
        Convert raw mathematical results into human-readable text.
        
        Args:
            q_type: Question type ('nash', 'csp', 'minmax')
            result: Raw result from core_logic solvers
            
        Returns:
            Formatted result string
        """
        if result is None:
            return "Nu s-a putut calcula o soluție."
        
        if q_type == 'nash':
            # Result is a list of tuples: [(row, col), ...]
            if not result:
                return "Nu există echilibre Nash pure în acest joc."
            
            if len(result) == 1:
                row, col = result[0]
                return f"Echilibrul Nash pur este la linia {row}, coloana {col}."
            else:
                coords_str = ", ".join([f"({r},{c})" for r, c in result])
                return f"Există {len(result)} echilibre Nash pure la pozițiile: {coords_str}."
        
        elif q_type == 'csp':
            # Result is a dict: {'A': 1, 'B': 2, ...} or None
            if not result or not isinstance(result, dict):
                return "Problema CSP nu are soluție (este inconsistentă)."
            
            assignments = ", ".join([f"{var}={val}" for var, val in sorted(result.items())])
            return f"Asignarea variabilelor: {assignments}."
        
        elif q_type == 'minmax':
            # Result can be a dict with 'root_value' and 'visited_count'
            # or a tuple (root_value, visited_count)
            if isinstance(result, dict):
                root_value = result.get('root_value')
                visited_count = result.get('visited_count')
                
                if root_value is not None and visited_count is not None:
                    return (f"Valoarea din rădăcină este {root_value}. "
                           f"Au fost vizitate {visited_count} noduri frunză.")
                elif root_value is not None:
                    return f"Valoarea din rădăcină este {root_value}."
                else:
                    return "Nu s-au putut calcula rezultatele MinMax."
            
            elif isinstance(result, tuple) and len(result) == 2:
                root_value, visited_count = result
                return (f"Valoarea din rădăcină este {root_value}. "
                       f"Au fost vizitate {visited_count} noduri frunză.")
            
            else:
                return f"Valoarea calculată: {result}."
        
        else:
            return f"Rezultat: {result}"
    
    def _get_theory_text(self, tags: List[str]) -> Optional[str]:
        """
        Find the most relevant theoretical concept from the knowledge base.
        
        Selects the concept with the highest tag overlap (intersection)
        with the provided tags.
        
        Args:
            tags: List of tags associated with the question
            
        Returns:
            Formatted theory text or None if no match found
        """
        if not self.knowledge_base or not tags:
            return None
        
        # Find concept with highest tag overlap
        best_match = None
        best_overlap = 0
        
        for concept_entry in self.knowledge_base:
            concept_tags = concept_entry.get('tags', [])
            
            # Calculate intersection
            overlap = len(set(tags) & set(concept_tags))
            
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = concept_entry
        
        if not best_match or best_overlap == 0:
            return None
        
        # Format the theory text
        concept_name = best_match.get('concept', 'Concept')
        definition = best_match.get('definition', '')
        source = best_match.get('source', 'Necunoscut')
        
        theory_text = f"Conform sursei [{source}], {concept_name}: {definition}"
        
        return theory_text
    
    def generate_full_answer(
        self, 
        q_type: str, 
        math_result: Any, 
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Generate a complete answer combining math results and theory.
        
        Args:
            q_type: Question type ('nash', 'csp', 'minmax')
            math_result: Raw mathematical result from solver
            tags: Optional list of tags for finding relevant theory
            
        Returns:
            Formatted complete answer string
        """
        # Format mathematical result
        formatted_result = self._format_math_result(q_type, math_result)
        
        # Build answer starting with the math result
        answer_parts = [
            "Răspuns Corect:",
            formatted_result
        ]
        
        # Add theoretical justification if tags provided
        if tags:
            theory_text = self._get_theory_text(tags)
            
            if theory_text:
                answer_parts.extend([
                    "",  # Empty line
                    "Justificare Teoretică:",
                    theory_text
                ])
        
        # Combine all parts
        full_answer = "\n".join(answer_parts)
        
        return full_answer
