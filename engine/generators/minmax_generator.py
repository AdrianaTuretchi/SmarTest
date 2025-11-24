from typing import Dict, Any, Optional
from core_logic.minmax_logic import generate_random_tree, tree_to_dict, Node


class MinMaxGenerator:
    def __init__(self, templates: Optional[Dict[str, Any]] = None):
        self.templates = templates or {}

    @staticmethod
    def _tree_to_string(node: Node, prefix: str = "", is_left: bool = True) -> str:
        if not node.children:
            return f"{prefix}{'└── ' if is_left else '┌── '}{node.value}\n"
        result = f"{prefix}{'└── ' if is_left else '┌── '}[ ]\n"
        result += MinMaxGenerator._tree_to_string(node.children[0], prefix + ("    " if is_left else "│   "), True)
        result += MinMaxGenerator._tree_to_string(node.children[1], prefix + ("    " if is_left else "│   "), False)
        return result

    def generate(self, depth: int = 3, max_leaf_value: int = 10, template_id: Optional[str] = None) -> Dict[str, Any]:
        tree = generate_random_tree(depth, max_leaf_value)
        question_text = (
            "Pentru arborele dat mai jos, aplică strategia MinMax cu optimizarea Alpha-Beta.\n"
            "Care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate?\n\n"
            f"{self._tree_to_string(tree)}"
        )

        raw_data = tree_to_dict(tree)

        return {
            "question_text": question_text,
            "raw_data": raw_data,
            "template_id": template_id,
        }
