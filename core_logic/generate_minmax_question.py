import random
from typing import List, Optional, Tuple

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

def minmax(node: Node, depth: int, alpha: int, beta: int, maximizing: bool, visited: List[int]) -> int:
    if not node.children:
        visited.append(node.value)
        return node.value

    if maximizing:
        max_eval = float('-inf')
        for child in node.children:
            eval = minmax(child, depth + 1, alpha, beta, False, visited)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            eval = minmax(child, depth + 1, alpha, beta, True, visited)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def tree_to_string(node: Node, prefix: str = "", is_left: bool = True) -> str:
    if not node.children:
        return f"{prefix}{'└── ' if is_left else '┌── '}{node.value}\n"
    result = f"{prefix}{'└── ' if is_left else '┌── '}[ ]\n"
    result += tree_to_string(node.children[0], prefix + ("    " if is_left else "│   "), True)
    result += tree_to_string(node.children[1], prefix + ("    " if is_left else "│   "), False)
    return result

def generate_minmax_tree_question(depth: int = 3) -> Tuple[str, int, int]:
    tree = generate_random_tree(depth)
    visited_leaves = []
    root_value = minmax(tree, 0, float('-inf'), float('inf'), True, visited_leaves)

    question_text = (
        "Pentru arborele dat mai jos, aplică strategia MinMax cu optimizarea Alpha-Beta.\n"
        "Care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate?\n\n"
        f"{tree_to_string(tree)}"
    )

    return question_text, root_value, len(visited_leaves)

#q, val, count = generate_minmax_tree_question()
#print(q)
#print(f"Valoare rădăcină: {val}")
#print(f"Noduri frunze vizitate: {count}")
