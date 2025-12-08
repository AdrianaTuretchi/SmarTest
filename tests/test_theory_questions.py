"""
Test script to demonstrate pure theory question generation.
Creates mock templates with 'requires_theory' tag (no data generation).
"""
import sys
from pathlib import Path

# Add parent directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from engine.generators.nash_generator import NashGenerator
from engine.generators.csp_generator import CSPGenerator
from engine.generators.minmax_generator import MinMaxGenerator


def test_pure_theory_questions():
    """Test generators with pure theory templates (no data generation)."""
    print("\n" + "="*70)
    print("PURE THEORY QUESTION GENERATION TEST")
    print("="*70)
    
    # Mock pure theory templates
    print("\n" + "-"*70)
    print("1. NASH - Pure Theory Template")
    print("-"*70)
    
    nash_theory_template = {
        "nash-theory-1": {
            "id": "nash-theory-1",
            "template": "Explicați conceptul de echilibru Nash. Cum diferă echilibrul Nash pur de cel mixt? Dați exemple din viața reală unde echilibrul Nash este aplicabil.",
            "tags": ["nash", "game-theory", "requires_theory"]
        }
    }
    
    nash_gen = NashGenerator(nash_theory_template)
    nash_result = nash_gen.generate()
    
    print(f"Template ID: {nash_result['template_id']}")
    print(f"Has raw_data: {nash_result['raw_data'] is not None}")
    print(f"\nQuestion Text:\n{nash_result['question_text']}")
    
    if nash_result['raw_data'] is None:
        print("\n✓ SUCCESS: No data generated (pure theory)")
    else:
        print("\n✗ FAILURE: Data was generated unexpectedly!")
    
    # Mock CSP theory template
    print("\n" + "-"*70)
    print("2. CSP - Pure Theory Template")
    print("-"*70)
    
    # Create a temporary JSON file with theory template
    import json
    import tempfile
    
    csp_theory_templates = [
        {
            "id": "csp-theory-1",
            "template": "Descrieți algoritmul de backtracking pentru CSP. Care sunt diferențele dintre Forward Checking și Arc Consistency? În ce situații este preferabil să folosim euristica MRV (Minimum Remaining Values)?",
            "tags": ["csp", "constraint-satisfaction", "requires_theory"]
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as tmp:
        json.dump(csp_theory_templates, tmp)
        tmp_path = tmp.name
    
    csp_gen = CSPGenerator(tmp_path)
    csp_result = csp_gen.generate(template_id="csp-theory-1")
    
    print(f"Template ID: {csp_result['template_id']}")
    print(f"Has raw_data: {csp_result['raw_data'] is not None}")
    print(f"\nQuestion Text:\n{csp_result['question_text']}")
    
    if csp_result['raw_data'] is None:
        print("\n✓ SUCCESS: No data generated (pure theory)")
    else:
        print("\n✗ FAILURE: Data was generated unexpectedly!")
    
    # Cleanup
    import os
    os.unlink(tmp_path)
    
    # Mock MinMax theory template
    print("\n" + "-"*70)
    print("3. MINMAX - Pure Theory Template")
    print("-"*70)
    
    minmax_theory_templates = [
        {
            "id": "minmax-theory-1",
            "template": "Explicați principiul de funcționare al algoritmului MinMax. Cum funcționează optimizarea Alpha-Beta și de ce reduce numărul de noduri evaluate? Care este complexitatea temporală a algoritmului MinMax fără și cu optimizarea Alpha-Beta?",
            "tags": ["minmax", "alpha-beta", "game-tree", "requires_theory"]
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as tmp:
        json.dump(minmax_theory_templates, tmp)
        tmp_path = tmp.name
    
    minmax_gen = MinMaxGenerator(tmp_path)
    minmax_result = minmax_gen.generate(template_id="minmax-theory-1")
    
    print(f"Template ID: {minmax_result['template_id']}")
    print(f"Has raw_data: {minmax_result['raw_data'] is not None}")
    print(f"\nQuestion Text:\n{minmax_result['question_text']}")
    
    if minmax_result['raw_data'] is None:
        print("\n✓ SUCCESS: No data generated (pure theory)")
    else:
        print("\n✗ FAILURE: Data was generated unexpectedly!")
    
    # Cleanup
    os.unlink(tmp_path)


def test_hybrid_questions():
    """Test generators with hybrid templates (data + theory)."""
    print("\n" + "="*70)
    print("HYBRID QUESTION GENERATION TEST")
    print("="*70)
    
    print("\n" + "-"*70)
    print("NASH - Hybrid Template")
    print("-"*70)
    
    nash_hybrid_template = {
        "nash-hybrid-1": {
            "id": "nash-hybrid-1",
            "template": "Pentru jocul de mai jos, identificați toate echilibrele Nash pure. Explicați de asemenea cum se poate extinde analiza pentru a include echilibre Nash mixte.",
            "tags": ["nash", "game-theory", "hybrid"]
        }
    }
    
    nash_gen = NashGenerator(nash_hybrid_template)
    nash_result = nash_gen.generate()
    
    print(f"Template ID: {nash_result['template_id']}")
    print(f"Has raw_data: {nash_result['raw_data'] is not None}")
    print(f"Question includes matrix: {'Matricea' in nash_result['question_text']}")
    
    if nash_result['raw_data'] is not None:
        print("\n✓ SUCCESS: Data generated (hybrid question)")
        print(f"Matrix dimensions: {len(nash_result['raw_data'])}x{len(nash_result['raw_data'][0])}")
    else:
        print("\n✗ FAILURE: No data was generated!")


def test_calculation_questions():
    """Test generators with pure calculation templates."""
    print("\n" + "="*70)
    print("PURE CALCULATION QUESTION GENERATION TEST")
    print("="*70)
    
    print("\n" + "-"*70)
    print("NASH - Calculation Template")
    print("-"*70)
    
    nash_calc_template = {
        "nash-calc-1": {
            "id": "nash-calc-1",
            "template": "Pentru matricea de plăți dată, găsiți toate echilibrele Nash pure:",
            "tags": ["nash", "game-theory", "requires_calculation"]
        }
    }
    
    nash_gen = NashGenerator(nash_calc_template)
    nash_result = nash_gen.generate()
    
    print(f"Template ID: {nash_result['template_id']}")
    print(f"Has raw_data: {nash_result['raw_data'] is not None}")
    
    if nash_result['raw_data'] is not None:
        print("\n✓ SUCCESS: Data generated (calculation question)")
        print(f"Matrix dimensions: {len(nash_result['raw_data'])}x{len(nash_result['raw_data'][0])}")
    else:
        print("\n✗ FAILURE: No data was generated!")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SEMANTIC TAGS - COMPREHENSIVE DEMONSTRATION")
    print("Testing: requires_theory, hybrid, requires_calculation")
    print("="*70)
    
    try:
        test_pure_theory_questions()
        test_hybrid_questions()
        test_calculation_questions()
        
        print("\n" + "="*70)
        print("✓ ALL DEMONSTRATIONS COMPLETED")
        print("="*70)
        print("\nSummary:")
        print("  - Pure Theory: No data generation (clean question text)")
        print("  - Hybrid: Data generation + theory explanation")
        print("  - Calculation: Data generation only")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
