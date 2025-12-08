import json
import random
from pathlib import Path
from typing import Dict, Any, Optional
from core_logic.minmax_logic import generate_random_tree, tree_to_dict, Node


class MinMaxGenerator:
    # Tags that trigger data generation
    DATA_TRIGGER_TAGS = {'requires_calculation', 'hybrid'}
    
    # Default fallback template if JSON file is empty or not found
    DEFAULT_TEMPLATE = (
        "Pentru arborele dat mai jos, aplică strategia MinMax cu optimizarea Alpha-Beta.\n"
        "Care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate?"
    )
    
    def __init__(self, templates_path: Optional[str] = None):
        self.minmax_templates = []
        
        if templates_path:
            try:
                with open(templates_path, 'r', encoding='utf-8') as f:
                    all_templates = json.load(f)
                # Filter templates that have 'minmax' in tags
                self.minmax_templates = [
                    t for t in all_templates 
                    if 'minmax' in t.get('tags', [])
                ]
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # Log warning but continue with empty list
                print(f"Warning: Could not load MinMax templates from {templates_path}: {e}")
                self.minmax_templates = []

    @staticmethod
    def _tree_to_string(node: Node, prefix: str = "", is_left: bool = True) -> str:
        if not node.children:
            return f"{prefix}{'└── ' if is_left else '┌── '}{node.value}\n"
        result = f"{prefix}{'└── ' if is_left else '┌── '}[ ]\n"
        result += MinMaxGenerator._tree_to_string(node.children[0], prefix + ("    " if is_left else "│   "), True)
        result += MinMaxGenerator._tree_to_string(node.children[1], prefix + ("    " if is_left else "│   "), False)
        return result

    def generate(self, depth: Optional[int] = None, max_leaf_value: Optional[int] = None, template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a MinMax question with optional parameters.
        
        Args:
            depth: Tree depth (default: random 2-4)
            max_leaf_value: Maximum leaf value (default: random 9-20)
            template_id: Specific template to use (default: random selection)
            
        Returns:
            Dictionary with question_text, raw_data, and template_id
        """
        # Select template
        selected_template = None
        
        if template_id and self.minmax_templates:
            # Try to find specific template by ID
            selected_template = next(
                (t for t in self.minmax_templates if t['id'] == template_id),
                None
            )
        
        if not selected_template and self.minmax_templates:
            # Random selection from available templates
            selected_template = random.choice(self.minmax_templates)
        
        # Use template text or fallback
        if selected_template:
            template_text = selected_template['template']
            final_template_id = selected_template['id']
            template_tags = set(selected_template.get('tags', []))
            # If template not found, assume it requires calculation (safe default)
            needs_data = True
        else:
            template_text = self.DEFAULT_TEMPLATE
            final_template_id = 'minmax-default'
            # Fallback always requires calculation
            needs_data = True
        
        # Check if data generation is needed (only if we have a real template)
        if selected_template:
            needs_data = bool(template_tags & self.DATA_TRIGGER_TAGS)
        
        if needs_data:
            # Generate random parameters if not provided
            if depth is None:
                depth = random.randint(2, 4)  # Random depth between 2 and 4
            if max_leaf_value is None:
                max_leaf_value = random.randint(9, 20)  # Random max value between 9 and 20
            
            # Generate and append data for calculation-based questions
            tree = generate_random_tree(depth, max_leaf_value)
            question_text = template_text + "\n\n" + self._tree_to_string(tree)
            raw_data = tree_to_dict(tree)
        else:
            # Pure theory question - no data generation
            question_text = template_text
            raw_data = None

        return {
            "question_text": question_text,
            "raw_data": raw_data,
            "template_id": final_template_id,
        }