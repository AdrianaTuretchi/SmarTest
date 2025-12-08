"""
Comprehensive test demonstrating the semantic tags workflow.
Shows the complete flow from templates to question generation.
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


def display_semantic_tag_logic():
    """Display the semantic tag logic rules."""
    print("\n" + "="*80)
    print("SEMANTIC TAGS LOGIC - IMPLEMENTATION RULES")
    print("="*80)
    
    print("""
The generators now respect semantic tags to conditionally generate data:

DATA_TRIGGER_TAGS = {'requires_calculation', 'hybrid'}

GENERATION LOGIC:
-----------------
1. Select Template: Choose from available templates with matching type tag
2. Check Tags: Extract tags from selected template
3. Conditional Generation:
   
   IF template.tags ∩ DATA_TRIGGER_TAGS ≠ ∅:
       → Generate random data (matrix/tree/CSP)
       → Format data as string
       → Append to template text
       → Set raw_data to generated structure
   
   ELSE (Pure Theory):
       → Skip data generation
       → question_text = template_text (clean)
       → raw_data = None

TAG SEMANTICS:
--------------
• 'requires_calculation' → Pure calculation problem (data always generated)
• 'hybrid'               → Mixed question (data + theory) (data generated)
• 'requires_theory'      → Pure theory question (NO data generation)
• (implicit)             → If no DATA_TRIGGER_TAGS present, treat as theory

FALLBACK BEHAVIOR:
------------------
• If no template found → Use DEFAULT_TEMPLATE
• Fallback always generates data (safe default for backward compatibility)
• This ensures existing workflows continue to work

BENEFITS:
---------
✓ Flexible question types (theory, calculation, hybrid)
✓ Cleaner question text for pure theory
✓ Explicit semantic meaning via tags
✓ Easy to extend with new tag types
✓ Backward compatible via fallback
    """)


def demonstrate_all_question_types():
    """Demonstrate all three question types with examples."""
    print("\n" + "="*80)
    print("QUESTION TYPE DEMONSTRATIONS")
    print("="*80)
    
    # Load actual templates
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    with open(templates_path, 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find examples of each type
    calculation_templates = [t for t in templates if 'requires_calculation' in t.get('tags', [])]
    hybrid_templates = [t for t in templates if 'hybrid' in t.get('tags', [])]
    
    print("\n" + "-"*80)
    print("1. PURE CALCULATION QUESTION")
    print("-"*80)
    if calculation_templates:
        example = calculation_templates[0]
        print(f"\nTemplate ID: {example['id']}")
        print(f"Tags: {example['tags']}")
        print(f"\nTemplate Text:\n{example['template'][:150]}...")
        print("\n→ Result: Data IS generated (matrix/tree/CSP appended)")
        print("→ raw_data: NOT None")
        print("→ Can be evaluated mathematically")
    
    print("\n" + "-"*80)
    print("2. HYBRID QUESTION (Calculation + Theory)")
    print("-"*80)
    if hybrid_templates:
        example = hybrid_templates[0]
        print(f"\nTemplate ID: {example['id']}")
        print(f"Tags: {example['tags']}")
        print(f"\nTemplate Text:\n{example['template'][:150]}...")
        print("\n→ Result: Data IS generated (matrix/tree/CSP appended)")
        print("→ raw_data: NOT None")
        print("→ Requires both calculation AND explanation")
    
    print("\n" + "-"*80)
    print("3. PURE THEORY QUESTION")
    print("-"*80)
    print("\nTemplate ID: (example - not in current templates.json)")
    print("Tags: ['nash', 'game-theory', 'requires_theory']")
    print("\nTemplate Text:")
    print("'Explicați conceptul de echilibru Nash și diferența dintre echilibrul pur și mixt.'")
    print("\n→ Result: Data is NOT generated")
    print("→ raw_data: None")
    print("→ Pure conceptual/theoretical question")


def show_generator_constants():
    """Show the DATA_TRIGGER_TAGS constant in each generator."""
    print("\n" + "="*80)
    print("GENERATOR CONSTANTS")
    print("="*80)
    
    print(f"\nNashGenerator.DATA_TRIGGER_TAGS = {NashGenerator.DATA_TRIGGER_TAGS}")
    print(f"CSPGenerator.DATA_TRIGGER_TAGS = {CSPGenerator.DATA_TRIGGER_TAGS}")
    print(f"MinMaxGenerator.DATA_TRIGGER_TAGS = {MinMaxGenerator.DATA_TRIGGER_TAGS}")
    
    print("\nAll generators use the same trigger tags for consistency.")


def show_code_example():
    """Show code snippet of the implementation."""
    print("\n" + "="*80)
    print("CODE IMPLEMENTATION EXAMPLE")
    print("="*80)
    
    code = '''
# Inside NashGenerator.generate() method:

# Select template
template_id = random.choice(list(self.nash_templates.keys()))
selected_template = self.nash_templates[template_id]
template_text = selected_template['template']
template_tags = set(selected_template.get('tags', []))

# Check if data generation is needed
needs_data = bool(template_tags & self.DATA_TRIGGER_TAGS)

if needs_data:
    # Generate and append data for calculation-based questions
    raw_matrix = self._generate_nash_data()
    formatted_matrix_str = self._format_matrix_as_string(raw_matrix)
    final_question_text = template_text + "\\n" + formatted_matrix_str
    raw_data = raw_matrix
else:
    # Pure theory question - no data generation
    final_question_text = template_text
    raw_data = None

return {
    "question_text": final_question_text,
    "raw_data": raw_data,
    "template_id": template_id,
}
    '''
    
    print(code)


def show_template_statistics():
    """Show statistics about current templates."""
    print("\n" + "="*80)
    print("CURRENT TEMPLATE STATISTICS")
    print("="*80)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    with open(templates_path, 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    total = len(templates)
    calculation = len([t for t in templates if 'requires_calculation' in t.get('tags', [])])
    hybrid = len([t for t in templates if 'hybrid' in t.get('tags', [])])
    theory = len([t for t in templates if 'requires_theory' in t.get('tags', [])])
    
    nash_count = len([t for t in templates if 'nash' in t.get('tags', [])])
    csp_count = len([t for t in templates if 'csp' in t.get('tags', [])])
    minmax_count = len([t for t in templates if 'minmax' in t.get('tags', [])])
    
    print(f"\nTotal Templates: {total}")
    print(f"\nBy Question Type:")
    print(f"  • Nash Equilibrium: {nash_count}")
    print(f"  • CSP: {csp_count}")
    print(f"  • MinMax: {minmax_count}")
    
    print(f"\nBy Semantic Tag:")
    print(f"  • requires_calculation: {calculation} ({calculation/total*100:.1f}%)")
    print(f"  • hybrid: {hybrid} ({hybrid/total*100:.1f}%)")
    print(f"  • requires_theory: {theory} ({theory/total*100:.1f}%)")
    
    print(f"\nData Generation:")
    print(f"  • Templates that trigger data: {calculation + hybrid} ({(calculation+hybrid)/total*100:.1f}%)")
    print(f"  • Templates that skip data: {theory} ({theory/total*100:.1f}%)")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("SEMANTIC TAGS - COMPLETE WORKFLOW DOCUMENTATION")
    print("="*80)
    
    try:
        display_semantic_tag_logic()
        show_generator_constants()
        demonstrate_all_question_types()
        show_code_example()
        show_template_statistics()
        
        print("\n" + "="*80)
        print("✓ DOCUMENTATION COMPLETE")
        print("="*80)
        print("\nNext Steps:")
        print("  1. Add 'requires_theory' templates to templates.json")
        print("  2. Update EvaluationService to handle raw_data=None cases")
        print("  3. Consider adding more semantic tags (difficulty levels, etc.)")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
