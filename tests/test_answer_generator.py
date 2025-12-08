"""
Test script for AnswerGenerator
Validates formatting and theory matching for all question types.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from engine.answer_generator import AnswerGenerator


def test_nash_answers():
    """Test Nash equilibrium answer generation."""
    print("\n" + "="*60)
    print("  NASH EQUILIBRIUM ANSWERS")
    print("="*60)
    
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    generator = AnswerGenerator(str(kb_path))
    
    # Test case 1: Single Nash equilibrium
    result1 = [(0, 1)]
    tags1 = ['nash', 'game-theory']
    answer1 = generator.generate_full_answer('nash', result1, tags1)
    print("\n--- Test 1: Single Equilibrium ---")
    print(answer1)
    
    # Test case 2: Multiple equilibria
    result2 = [(0, 0), (1, 1)]
    answer2 = generator.generate_full_answer('nash', result2, tags1)
    print("\n--- Test 2: Multiple Equilibria ---")
    print(answer2)
    
    # Test case 3: No equilibrium
    result3 = []
    answer3 = generator.generate_full_answer('nash', result3, tags1)
    print("\n--- Test 3: No Equilibrium ---")
    print(answer3)


def test_csp_answers():
    """Test CSP answer generation."""
    print("\n" + "="*60)
    print("  CSP ANSWERS")
    print("="*60)
    
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    generator = AnswerGenerator(str(kb_path))
    
    # Test case 1: Valid solution
    result1 = {'A': 1, 'B': 2, 'C': 3}
    tags1 = ['csp', 'backtracking']
    answer1 = generator.generate_full_answer('csp', result1, tags1)
    print("\n--- Test 1: Valid Solution ---")
    print(answer1)
    
    # Test case 2: No solution (None)
    result2 = None
    answer2 = generator.generate_full_answer('csp', result2, tags1)
    print("\n--- Test 2: No Solution ---")
    print(answer2)
    
    # Test case 3: Empty dict
    result3 = {}
    answer3 = generator.generate_full_answer('csp', result3, tags1)
    print("\n--- Test 3: Empty Assignment ---")
    print(answer3)


def test_minmax_answers():
    """Test MinMax answer generation."""
    print("\n" + "="*60)
    print("  MINMAX ANSWERS")
    print("="*60)
    
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    generator = AnswerGenerator(str(kb_path))
    
    # Test case 1: Dict format
    result1 = {'root_value': 5, 'visited_count': 10}
    tags1 = ['minmax', 'alpha-beta']
    answer1 = generator.generate_full_answer('minmax', result1, tags1)
    print("\n--- Test 1: Dict Format ---")
    print(answer1)
    
    # Test case 2: Tuple format
    result2 = (7, 8)
    answer2 = generator.generate_full_answer('minmax', result2, tags1)
    print("\n--- Test 2: Tuple Format ---")
    print(answer2)
    
    # Test case 3: Only root value
    result3 = {'root_value': 3}
    answer3 = generator.generate_full_answer('minmax', result3, tags1)
    print("\n--- Test 3: Only Root Value ---")
    print(answer3)


def test_theory_matching():
    """Test theory matching with different tag combinations."""
    print("\n" + "="*60)
    print("  THEORY MATCHING")
    print("="*60)
    
    kb_path = project_root / "assets" / "json_output" / "knowledge_base.json"
    generator = AnswerGenerator(str(kb_path))
    
    test_cases = [
        (['nash', 'game-theory'], 'Nash + Game Theory'),
        (['csp', 'backtracking'], 'CSP + Backtracking'),
        (['minmax', 'alpha-beta'], 'MinMax + Alpha-Beta'),
        (['game-theory', 'pareto'], 'Pareto Optimality'),
        (['unknown', 'tags'], 'Unknown Tags'),
    ]
    
    for tags, description in test_cases:
        theory = generator._get_theory_text(tags)
        print(f"\n--- {description} ---")
        print(f"Tags: {tags}")
        if theory:
            print(f"Match: {theory[:100]}...")
        else:
            print("Match: None")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  ANSWER GENERATOR TEST SUITE")
    print("="*60)
    
    test_nash_answers()
    test_csp_answers()
    test_minmax_answers()
    test_theory_matching()
    
    print("\n" + "="*60)
    print("  ALL TESTS COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
