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
            q_type: Question type ('nash', 'csp', 'minmax', 'strategy')
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
            if isinstance(result, dict) and result:
                assignments = ", ".join([f"{var}={val}" for var, val in sorted(result.items())])
                return f"Soluție găsită: {assignments}."
            else:
                return "Problema CSP nu are soluție (este inconsistentă)."

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

        elif q_type == 'strategy':

            # Ensure result is a tuple (score, feedback)
            if isinstance(result, float):
                result = (result, "Strategia a fost evaluată cu succes.")

            # Validate score and generate feedback
            if isinstance(result, tuple) and len(result) == 2:
                score, feedback = result

                # Check if score is valid (e.g., greater than 0)
                if score > 0:
                    return feedback  # Return the feedback directly
                else:
                    return "Strategia selectată nu este corectă."
            else:
                return "Strategia selectată nu este corectă."

        else:
            return f"Rezultat: {result}"
    
    def _get_theory_text(self, tags: List[str], template_id: Optional[str] = None) -> Optional[str]:
        """
        Find the most relevant theoretical concept from the knowledge base.

        Prioritizes concepts with the exact question tag (e.g., 'csp-3').
        If no exact match is found, falls back to the highest tag overlap.

        Args:
            tags: List of tags associated with the question
            template_id: Optional template ID for more specific matching

        Returns:
            Formatted theory text or None if no match found
        """
        if not self.knowledge_base or not tags:
            return None
        
        # Step 1: Check for exact match with template_id
        if template_id:
            for concept_entry in self.knowledge_base:
                concept_tags = concept_entry.get('tags', [])
                if template_id in concept_tags:
                    # Format the theory text for the exact match
                    concept_name = concept_entry.get('concept', 'Concept')
                    definition = concept_entry.get('definition', '')
                    source = concept_entry.get('source', 'Necunoscut')
                    return f"Conform sursei [{source}], {concept_name}: {definition}"

        # Step 2: Check for exact match with specific ID (e.g., 'use_nash')
        specific_tags = [tag for tag in tags if tag.startswith("use_")]
        for concept_entry in self.knowledge_base:
            concept_tags = concept_entry.get('tags', [])
            if any(specific_tag in concept_tags for specific_tag in specific_tags):
                # Format the theory text for the exact match
                concept_name = concept_entry.get('concept', 'Concept')
                definition = concept_entry.get('definition', '')
                source = concept_entry.get('source', 'Necunoscut')
                return f"Conform sursei [{source}], {concept_name}: {definition}"

        # Step 3: Fall back to highest tag overlap, explicitly prioritizing problem_type
        best_matches = []
        best_overlap = 0

        # Extract problem_type from tags
        problem_type = next((tag for tag in tags if tag in ["hanoi", "nash", "csp", "minmax", "strategy", "search", "graph-coloring", "knights-tour"]), None)

        for concept_entry in self.knowledge_base:
            concept_tags = concept_entry.get('tags', [])
            overlap = len(set(tags) & set(concept_tags))

            if problem_type and problem_type in concept_tags:
                overlap += 2  # Boost relevance for matching problem_type

            if overlap > best_overlap:
                best_overlap = overlap
                best_matches = [concept_entry]
            elif overlap == best_overlap:
                best_matches.append(concept_entry)

        if not best_matches or best_overlap == 0:
            return None

        # Step 4: Resolve ties among best matches
        if len(best_matches) > 1:
            best_matches = sorted(
                best_matches,
                key=lambda entry: (
                    problem_type in entry.get('tags', []),  # Prioritize problem_type match
                    -len(entry.get('tags', []))  # Prefer shorter tag lists (more specific)
                ),
                reverse=True
            )

        # Format the theory text for the best match
        selected_concept = best_matches[0]
        concept_name = selected_concept.get('concept', 'Concept')
        definition = selected_concept.get('definition', '')
        source = selected_concept.get('source', 'Necunoscut')

        return f"Conform sursei [{source}], {concept_name}: {definition}"
    
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
        # Initialize answer_parts with a default value
        answer_parts = ["Răspuns Invalid:", "Nu s-a putut genera un răspuns complet."]

        # Format mathematical result
        formatted_result = self._format_math_result(q_type, math_result)

        # Ensure problem_type is included in tags
        if q_type not in tags:
            tags = tags + [q_type] if tags else [q_type]

        # Determine the prefix based on the validity of the result
        if "Strategia selectată nu este corectă." in formatted_result:
            answer_parts = [
                "Răspuns Gresit:",
                formatted_result
            ]
        else:
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
