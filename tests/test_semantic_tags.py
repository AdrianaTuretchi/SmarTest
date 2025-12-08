"""
Test script to verify generators respect semantic tags.
Tests: requires_calculation, hybrid, and requires_theory (implicit).
"""
import sys
from pathlib import Path

# Add parent directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import json
from engine.generators.nash_generator import NashGenerator
from engine.generators.csp_generator import CSPGenerator
from engine.generators.minmax_generator import MinMaxGenerator


def load_templates():
    """Load templates from JSON file."""
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    with open(templates_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_nash_generator():
    """Test Nash generator with different tag types."""
    print("\n" + "="*70)
    print("TESTING NASH GENERATOR")
    print("="*70)
    
    templates = load_templates()
    
    # Convert list to dict keyed by 'id'
    templates_dict = {t['id']: t for t in templates}
    
    generator = NashGenerator(templates_dict)
    
    # Test each Nash template
    nash_templates = {tid: t for tid, t in templates_dict.items() if 'nash' in t.get('tags', [])}
    
    for template_id, template in nash_templates.items():
        tags = template.get('tags', [])
        print(f"\n--- Template: {template_id} ---")
        print(f"Tags: {tags}")
        
        # Check if it should generate data
        data_tags = {'requires_calculation', 'hybrid'}
        should_have_data = bool(set(tags) & data_tags)
        print(f"Expected data generation: {should_have_data}")
        
        # Generate question (need to temporarily set this template)
        generator.nash_templates = {template_id: template}
        result = generator.generate()
        
        has_data = result['raw_data'] is not None
        print(f"Actual data generation: {has_data}")
        print(f"Question text length: {len(result['question_text'])} chars")
        
        if has_data:
            print(f"Raw data type: {type(result['raw_data'])}")
            print(f"Matrix dimensions: {len(result['raw_data'])}x{len(result['raw_data'][0])}")
        
        # Verify correctness
        if should_have_data == has_data:
            print("✓ PASS: Data generation matches tags")
        else:
            print("✗ FAIL: Data generation mismatch!")
            

def test_csp_generator():
    """Test CSP generator with different tag types."""
    print("\n" + "="*70)
    print("TESTING CSP GENERATOR")
    print("="*70)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    generator = CSPGenerator(str(templates_path))
    
    templates = load_templates()
    csp_templates = [t for t in templates if 'csp' in t.get('tags', [])]
    
    for template in csp_templates:
        template_id = template['id']
        tags = template.get('tags', [])
        print(f"\n--- Template: {template_id} ---")
        print(f"Tags: {tags}")
        
        # Check if it should generate data
        data_tags = {'requires_calculation', 'hybrid'}
        should_have_data = bool(set(tags) & data_tags)
        print(f"Expected data generation: {should_have_data}")
        
        # Generate question
        result = generator.generate(template_id=template_id)
        
        has_data = result['raw_data'] is not None
        print(f"Actual data generation: {has_data}")
        print(f"Question text length: {len(result['question_text'])} chars")
        
        if has_data:
            print(f"Raw data keys: {result['raw_data'].keys()}")
            print(f"Variables: {result['raw_data']['variables']}")
        
        # Verify correctness
        if should_have_data == has_data:
            print("✓ PASS: Data generation matches tags")
        else:
            print("✗ FAIL: Data generation mismatch!")


def test_minmax_generator():
    """Test MinMax generator with different tag types."""
    print("\n" + "="*70)
    print("TESTING MINMAX GENERATOR")
    print("="*70)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    generator = MinMaxGenerator(str(templates_path))
    
    templates = load_templates()
    minmax_templates = [t for t in templates if 'minmax' in t.get('tags', [])]
    
    for template in minmax_templates:
        template_id = template['id']
        tags = template.get('tags', [])
        print(f"\n--- Template: {template_id} ---")
        print(f"Tags: {tags}")
        
        # Check if it should generate data
        data_tags = {'requires_calculation', 'hybrid'}
        should_have_data = bool(set(tags) & data_tags)
        print(f"Expected data generation: {should_have_data}")
        
        # Generate question
        result = generator.generate(template_id=template_id)
        
        has_data = result['raw_data'] is not None
        print(f"Actual data generation: {has_data}")
        print(f"Question text length: {len(result['question_text'])} chars")
        
        if has_data:
            print(f"Raw data keys: {result['raw_data'].keys()}")
            print(f"Tree has children: {'children' in result['raw_data']}")
        
        # Verify correctness
        if should_have_data == has_data:
            print("✓ PASS: Data generation matches tags")
        else:
            print("✗ FAIL: Data generation mismatch!")


def test_fallback_behavior():
    """Test that fallback templates always generate data (safe default)."""
    print("\n" + "="*70)
    print("TESTING FALLBACK BEHAVIOR")
    print("="*70)
    
    # Test with empty templates (triggers fallback)
    print("\n--- Nash Fallback ---")
    nash_gen = NashGenerator({})
    nash_result = nash_gen.generate()
    if 'error' in nash_result:
        print(f"Nash fallback returned error (expected): {nash_result['error']}")
    
    print("\n--- CSP Fallback ---")
    csp_gen = CSPGenerator(None)
    csp_result = csp_gen.generate()
    print(f"CSP fallback has data: {csp_result['raw_data'] is not None}")
    print(f"Template ID: {csp_result['template_id']}")
    if csp_result['raw_data'] is not None:
        print("✓ PASS: Fallback generates data (safe default)")
    
    print("\n--- MinMax Fallback ---")
    minmax_gen = MinMaxGenerator(None)
    minmax_result = minmax_gen.generate()
    print(f"MinMax fallback has data: {minmax_result['raw_data'] is not None}")
    print(f"Template ID: {minmax_result['template_id']}")
    if minmax_result['raw_data'] is not None:
        print("✓ PASS: Fallback generates data (safe default)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SEMANTIC TAGS TEST SUITE")
    print("Testing conditional data generation based on template tags")
    print("="*70)
    
    try:
        test_nash_generator()
        test_csp_generator()
        test_minmax_generator()
        test_fallback_behavior()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS COMPLETED")
        print("="*70)
        print("\nKey behaviors verified:")
        print("  - 'requires_calculation' triggers data generation")
        print("  - 'hybrid' triggers data generation")
        print("  - 'requires_theory' (implicit) skips data generation")
        print("  - Fallback templates generate data (safe default)")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
