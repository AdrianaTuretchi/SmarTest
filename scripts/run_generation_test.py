import os
import sys
import json
from pathlib import Path

# Asiguram ca radacina proiectului este in sys.path atunci cand rulam din scripts/
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importăm modulele pe care vrem să le testăm (acum că project_root e în sys.path)
from engine.question_generator import QuestionGenerator
from core_logic.nash_equilibrium import find_pure_nash

def main_test():
    """
    Testează fluxul complet ONLINE:
    1. Generează o întrebare Nash.
    2. Rezolvă acea întrebare cu 'core_logic'.
    """
    print("--- Începe Testul de Generare și Rezolvare ---")

    # Calea către șabloanele noastre curate (construim din radacina proiectului)
    templates_path = project_root.joinpath("assets", "json_output", "templates.json")

    # 1. Inițializează generatorul
    q_generator = QuestionGenerator(templates_path)

    # 2. Generează mai multe întrebări de tip 'nash' (ex: 5)
    num_to_generate = 5
    for idx in range(1, num_to_generate + 1):
        print(f"\n=== Generare întrebarea #{idx} ===")
        generated_output = q_generator.generate_question_by_type("nash")

        if "error" in generated_output:
            print(f"EROARE: {generated_output['error']}")
            continue

        print("--- ÎNTREBARE GENERATĂ ---")
        print(generated_output['question_text'])

        # 3. Rezolvă întrebarea folosind datele brute
        raw_matrix = generated_output.get('raw_data')

        print("\n--- REZOLVARE (din core_logic) ---")
        solution = find_pure_nash(raw_matrix)

        if not solution:
            print("Răspuns corect: Nu există echilibre Nash pure.")
        else:
            print(f"Răspuns corect: Echilibrele se găsesc la coordonatele: {solution}")

    print("\n--- Testul de Generare și Rezolvare s-a încheiat ---")

if __name__ == "__main__":
    main_test()