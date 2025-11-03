import os
import sys
from pathlib import Path

# Asiguram ca radacina proiectului este in sys.path atunci cand scriptul
# este rulat din folderul `scripts/`. Fara asta, importul `utils` nu
# va fi gasit pentru ca Python adauga in sys.path doar folderul curent.
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importam functiile pe care tocmai le-am creat
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_raw_text, segment_questions
import json
from engine.template_miner import process_raw_questions

def main_extraction_test():
    """
    Functie principala pentru a testa fluxul de extragere si curatare.
    """
    print("--- Incepem testul de extragere PDF ---")

    # --- PASUL 1: Defineste un fisier de test ---
    # Asigura-te ca ai adaugat un fisier aici!
    test_file_name = "examen.pdf"
    # Construim calea absoluta din radacina proiectului, astfel incat
    # scriptul sa functioneze indiferent din ce director este apelat.
    test_file_path = project_root.joinpath("assets", "pdfs", "examene", test_file_name)

    # --- PASUL 2: Extrage textul brut ---
    print(f"Se extrage textul din: {test_file_path}")
    # pdf_parser asteapta un str, nu un Path, si verifica existenta fisierului
    raw_text = extract_text_from_pdf(str(test_file_path))

    if "Eroare:" in raw_text:
        print(raw_text)
        return

    # Afisam tot textul brut extras (poate fi lung) pentru inspectie
    print("Textul brut extras:\n")
    print(raw_text)
    print("\n" + "="*50 + "\n")

    # --- PASUL 3: Curata textul ---
    print("Se curata textul...")
    clean_text = clean_raw_text(raw_text)

    print("Textul curatat:\n")
    print(clean_text)

    # --- PASUL 4: Segmentare intrebari (daca exista) ---
    print("\nSe segmenteaza intrebari (daca se detecteaza):")
    questions = segment_questions(clean_text)
    if questions:
        print(f"Am detectat {len(questions)} intrebari. Afisare:")
        for i, q in enumerate(questions, start=1):
            print("\n--- INTREBARE", i, "---")
            print(q)

        # Salvam intrebari in JSON in assets/json_output
        out_dir = project_root.joinpath("assets", "json_output")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir.joinpath(f"{test_file_name}_questions.json")
        with open(out_file, "w", encoding="utf-8") as fh:
            json.dump({"source": str(test_file_path), "count": len(questions), "questions": questions}, fh, ensure_ascii=False, indent=2)
        print(f"\nIntrebările au fost salvate în: {out_file}")
        # --- PASUL 5: Procesare sabloane (template mining) ---
        try:
            templates = process_raw_questions(questions)
            templates_out = project_root.joinpath("assets", "json_output", "templates.json")
            with open(templates_out, "w", encoding="utf-8") as tf:
                json.dump(templates, tf, ensure_ascii=False, indent=2)
            print(f"Șabloanele extrase au fost salvate în: {templates_out}")
        except Exception as e:
            print(f"Eroare la procesarea sabloanelor: {e}")
    else:
        print("Nu s-au detectat intrebari numerotate în text.")

    print("\n--- Testul de extragere s-a incheiat ---")

if __name__ == "__main__":
    # Rulam functia principala doar cand scriptul este executat direct
    main_extraction_test()