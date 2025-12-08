"""
Example integration of AnswerGenerator with evaluation endpoints.

This shows how to use the AnswerGenerator to create smart answers
that combine mathematical results with theoretical justifications.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from engine.answer_generator import AnswerGenerator
from core_logic.nash_logic import find_pure_nash
from core_logic.csp_logic import backtrack
from core_logic.minmax_logic import dict_to_tree, minmax


def example_nash_evaluation():
    """Example: Nash equilibrium evaluation with smart answer."""
    print("\n" + "="*60)
    print("  EXAMPLE: Nash Equilibrium Evaluation")
    print("="*60)
    
    # Simulated user submission
    user_answer = "(0, 1)"
    raw_data = [
        [(3, 2), (1, 4)],
        [(2, 1), (4, 3)]
    ]
    tags = ['nash', 'game-theory']
    
    # Calculate correct answer
    correct_coords = find_pure_nash(raw_data)
    
    # Generate smart answer
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    answer_gen = AnswerGenerator(str(kb_path))
    smart_answer = answer_gen.generate_full_answer('nash', correct_coords, tags)
    
    print("\nUser submitted:", user_answer)
    print("\nSmart Answer Generated:")
    print("-" * 60)
    print(smart_answer)
    print("-" * 60)


def example_csp_evaluation():
    """Example: CSP evaluation with smart answer."""
    print("\n" + "="*60)
    print("  EXAMPLE: CSP Evaluation")
    print("="*60)
    
    # Simulated CSP problem
    variables = ['A', 'B', 'C']
    domains = {'A': [1, 2], 'B': [1, 2], 'C': [1, 2]}
    constraints = [('A', 'B'), ('B', 'C')]
    partial = {}
    tags = ['csp', 'backtracking']
    
    # Calculate correct solution
    correct_solution = backtrack(variables, domains, constraints, partial)
    
    # Generate smart answer
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    answer_gen = AnswerGenerator(str(kb_path))
    smart_answer = answer_gen.generate_full_answer('csp', correct_solution, tags)
    
    print("\nProblem:", variables, domains)
    print("\nSmart Answer Generated:")
    print("-" * 60)
    print(smart_answer)
    print("-" * 60)


def example_minmax_evaluation():
    """Example: MinMax evaluation with smart answer."""
    print("\n" + "="*60)
    print("  EXAMPLE: MinMax Evaluation")
    print("="*60)
    
    # Simulated tree data
    tree_dict = {
        "value": None,
        "children": [
            {"value": None, "children": [
                {"value": 3, "children": []},
                {"value": 5, "children": []}
            ]},
            {"value": None, "children": [
                {"value": 2, "children": []},
                {"value": 9, "children": []}
            ]}
        ]
    }
    tags = ['minmax', 'alpha-beta']
    
    # Reconstruct tree and calculate
    tree = dict_to_tree(tree_dict)
    visited = []
    root_value = minmax(tree, 0, float('-inf'), float('inf'), True, visited)
    
    result = {
        'root_value': root_value,
        'visited_count': len(visited)
    }
    
    # Generate smart answer
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    answer_gen = AnswerGenerator(str(kb_path))
    smart_answer = answer_gen.generate_full_answer('minmax', result, tags)
    
    print("\nTree processed")
    print("\nSmart Answer Generated:")
    print("-" * 60)
    print(smart_answer)
    print("-" * 60)


def main():
    """Run all integration examples."""
    print("\n" + "="*60)
    print("  ANSWER GENERATOR INTEGRATION EXAMPLES")
    print("="*60)
    
    example_nash_evaluation()
    example_csp_evaluation()
    example_minmax_evaluation()
    
    print("\n" + "="*60)
    print("  INTEGRATION EXAMPLES COMPLETE")
    print("="*60)
    print("\nThese examples show how to integrate AnswerGenerator")
    print("into your FastAPI evaluation endpoints to provide")
    print("comprehensive answers with theoretical justifications.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
