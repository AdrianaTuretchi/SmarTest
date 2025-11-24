from typing import List, Optional, Dict, Any
import random


class Node:
    def __init__(self, value: Optional[int] = None, children: Optional[List['Node']] = None):
        self.value = value
        self.children = children or []


def generate_random_tree(depth: int, max_leaf_value: int = 10) -> Node:
    if depth == 0:
        return Node(value=random.randint(0, max_leaf_value))
    return Node(children=[
        generate_random_tree(depth - 1, max_leaf_value),
        generate_random_tree(depth - 1, max_leaf_value)
    ])


def minmax(node: Node, depth: int, alpha: float, beta: float, maximizing: bool, visited: List[int]) -> int:
    if not node.children:
        visited.append(node.value)
        return node.value

    if maximizing:
        max_eval = float('-inf')
        for child in node.children:
            eval_v = minmax(child, depth + 1, alpha, beta, False, visited)
            max_eval = max(max_eval, eval_v)
            alpha = max(alpha, eval_v)
            if beta <= alpha:
                break
        return int(max_eval)
    else:
        min_eval = float('inf')
        for child in node.children:
            eval_v = minmax(child, depth + 1, alpha, beta, True, visited)
            min_eval = min(min_eval, eval_v)
            beta = min(beta, eval_v)
            if beta <= alpha:
                break
        return int(min_eval)


def tree_to_dict(node: Node) -> Dict[str, Any]:
    """Convert Node tree to a JSON-serializable dict."""
    return {
        "value": node.value,
        "children": [tree_to_dict(c) for c in node.children] if node.children else []
    }


def dict_to_tree(data: Dict[str, Any]) -> Node:
    """Reconstruct Node tree from dict created by `tree_to_dict`."""
    if data is None:
        return Node()
    value = data.get("value")
    children = [dict_to_tree(c) for c in data.get("children", [])]
    return Node(value=value, children=children)
