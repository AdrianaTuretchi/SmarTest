"""
Test script to validate template extraction logic for Nash, CSP, and MinMax questions.
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from engine.template_miner import process_raw_questions

# Sample questions for testing - with VARIED PHRASINGS from actual exams
test_questions = [
    # Nash question - variation 1: "echilibru nash" (singular)
    """3. (1p) Pentru jocul de mai jos, există echilibru Nash? Justificați.
    A B a b c a 1 2 2 3 1 1 b 2 2 3 3 1 1""",
    
    # Nash question - variation 2: "strategii dominate"
    """5. (1p) Pentru jocul de mai jos există strategii dominate pentru cel puțin unul din cei doi jucători?
    Mario Luigi Jump Stay Run Jump 3 1 2 3 1 4 Stay 1 1 4 2 1 4""",
    
    # CSP question - variation 1: "Forward checking" (no "asignarea variabilelor")
    """4. (2p) Aplicați algoritmul de Forward checking pentru următoarea problemă.
    Variabile: X1, X2, X3
    Domenii: D(X1) = {1, 2}, D(X2) = {1, 2}, D(X3) = {2, 3}""",
    
    # CSP question - variation 2: "satisfacere a restricțiilor"
    """6. (2p) Rezolvați următoarea problemă de satisfacere a restricțiilor.
    Graful: X1 -- X2 -- X3
    Domenii: toate variabilele au {1, 2, 3}""",
    
    # CSP question - variation 3: "Arc consistency"
    """7. (1p) Aplicați Arc consistency (AC-3) pe următorul graf de constrângeri.
    Variabile: A, B, C
    Domenii: D(A) = {1, 2}, D(B) = {2, 3}""",
    
    # MinMax question - variation 1: "MIN-MAX" with dash
    """8. (2p) Aplicați strategiei MIN-MAX cu Alpha-Beta pe arborele dat.
    Care este valoarea rădăcinii?
         [ ]
        /   \\
      [ ]   [ ]""",
    
    # MinMax question - variation 2: "MINIMAX" no dash
    """9. (2p) Pentru arborele de mai jos, folosiți algoritmul MINIMAX cu AlphaBeta pruning.
    Câte noduri frunze vor fi vizitate?
         [ ]""",
]

def main():
    print("=" * 60)
    print("  TEST: Template Extraction Logic")
    print("=" * 60)
    
    templates = process_raw_questions(test_questions)
    
    print(f"\n✓ Extracted {len(templates)} templates\n")
    
    for tmpl in templates:
        print(f"ID: {tmpl['id']}")
        print(f"Tags: {', '.join(tmpl['tags'])}")
        print(f"Template:\n  {tmpl['template'][:100]}...")
        print("-" * 60)
    
    # Statistics
    stats = {}
    for tmpl in templates:
        template_type = tmpl['id'].split('-')[0]
        stats[template_type] = stats.get(template_type, 0) + 1
    
    print("\n📊 Statistics:")
    print(f"   Nash: {stats.get('nash', 0)}")
    print(f"   CSP: {stats.get('csp', 0)}")
    print(f"   MinMax: {stats.get('minmax', 0)}")
    
    # Validation
    expected = {'nash': 2, 'csp': 3, 'minmax': 2}
    if stats == expected:
        print("\n✅ All template types extracted correctly!")
        print("   - Robust patterns working with varied phrasings")
    else:
        print(f"\n⚠️  Expected {expected}, got {stats}")

if __name__ == "__main__":
    main()
