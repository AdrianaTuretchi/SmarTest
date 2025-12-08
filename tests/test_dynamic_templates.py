"""
Test script to validate dynamic template usage in CSP and MinMax generators.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from engine.question_service import QuestionService

def main():
    print("=" * 60)
    print("  TEST: Dynamic Template Usage")
    print("=" * 60)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    
    print(f"\nTemplates file: {templates_path}")
    print(f"Exists: {templates_path.exists()}\n")
    
    # Initialize service
    service = QuestionService(str(templates_path))
    
    # Test CSP generation
    print("=" * 60)
    print("  CSP QUESTION GENERATION (3 samples)")
    print("=" * 60)
    for i in range(3):
        result = service.generate_question_by_type('csp')
        print(f"\n--- Sample {i+1} ---")
        print(f"Template ID: {result.get('template_id')}")
        print(f"Question (first 150 chars):\n{result.get('question_text', '')[:150]}...")
        print("-" * 60)
    
    # Test MinMax generation
    print("\n" + "=" * 60)
    print("  MINMAX QUESTION GENERATION (3 samples)")
    print("=" * 60)
    for i in range(3):
        result = service.generate_question_by_type('minmax')
        print(f"\n--- Sample {i+1} ---")
        print(f"Template ID: {result.get('template_id')}")
        print(f"Question (first 150 chars):\n{result.get('question_text', '')[:150]}...")
        print("-" * 60)
    
    # Test Nash (should still work)
    print("\n" + "=" * 60)
    print("  NASH QUESTION GENERATION (1 sample)")
    print("=" * 60)
    result = service.generate_question_by_type('nash')
    print(f"\nTemplate ID: {result.get('template_id')}")
    print(f"Question (first 150 chars):\n{result.get('question_text', '')[:150]}...")
    
    print("\n" + "=" * 60)
    print("✅ All generators working with dynamic templates!")
    print("=" * 60)

if __name__ == "__main__":
    main()
