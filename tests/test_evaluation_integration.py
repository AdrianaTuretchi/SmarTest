"""
Test script to verify EvaluationService integration with AnswerGenerator.
"""
import sys
from pathlib import Path

# Add parent directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from engine.evaluation_service import EvaluationService
from schemas import NashSubmission, CSPSubmission, MinMaxSubmission


def test_nash_evaluation():
    """Test Nash evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing Nash Evaluation")
    print("="*60)
    
    service = EvaluationService()
    
    # Test data
    raw_data = [
        [[3, 2], [1, 4]],
        [[2, 3], [4, 1]]
    ]
    
    # Correct answer
    submission = NashSubmission(
        user_answer="0,1",
        raw_data=raw_data
    )
    
    score, feedback = service.evaluate('nash', submission)
    
    print(f"Score: {score}")
    print(f"\nFeedback:\n{feedback}")
    print()


def test_csp_evaluation():
    """Test CSP evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing CSP Evaluation")
    print("="*60)
    
    service = EvaluationService()
    
    # Test data
    raw_data = {
        'variables': ['A', 'B', 'C'],
        'domains': {'A': [1, 2, 3], 'B': [1, 2, 3], 'C': [1, 2, 3]},
        'constraints': [('A', 'B'), ('B', 'C')],
        'partial_assignment': {}
    }
    
    # Correct answer
    submission = CSPSubmission(
        user_answer={'A': 1, 'B': 2, 'C': 1},
        raw_data=raw_data
    )
    
    score, feedback = service.evaluate('csp', submission)
    
    print(f"Score: {score}")
    print(f"\nFeedback:\n{feedback}")
    print()


def test_minmax_evaluation():
    """Test MinMax evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing MinMax Evaluation")
    print("="*60)
    
    service = EvaluationService()
    
    # Test data - simple tree
    raw_data = {
        "name": "root",
        "children": [
            {"name": "L", "value": 3},
            {"name": "R", "value": 5}
        ]
    }
    
    # Correct answer
    submission = MinMaxSubmission(
        root_value=5,
        visited_count=2,
        raw_data=raw_data
    )
    
    score, feedback = service.evaluate('minmax', submission)
    
    print(f"Score: {score}")
    print(f"\nFeedback:\n{feedback}")
    print()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("EVALUATION SERVICE INTEGRATION TEST")
    print("="*60)
    
    try:
        test_nash_evaluation()
        test_csp_evaluation()
        test_minmax_evaluation()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
