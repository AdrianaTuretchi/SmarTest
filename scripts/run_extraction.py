import os
import sys
from pathlib import Path
import json
from typing import List, Dict, Set

# Asiguram ca radacina proiectului este in sys.path atunci cand scriptul
# este rulat din folderul `scripts/`. Fara asta, importul `utils` nu
# va fi gasit pentru ca Python adauga in sys.path doar folderul curent.
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importam functiile pe care tocmai le-am creat
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_raw_text, segment_questions
from engine.template_miner import process_raw_questions


def process_single_pdf(pdf_path: Path) -> List[Dict]:
    """
    Procesează un singur PDF și returnează lista de șabloane extrase.
    
    Args:
        pdf_path: Calea către fișierul PDF
        
    Returns:
        Lista de șabloane (dict-uri cu id, template, tags, etc.)
    """
    print(f"\n{'='*60}")
    print(f"Procesare: {pdf_path.name}")
    print('='*60)
    
    # Extrage textul brut
    raw_text = extract_text_from_pdf(str(pdf_path))
    
    if "Eroare:" in raw_text:
        print(f"  ⚠️  Eroare la extragere: {raw_text}")
        return []
    
    print(f"  ✓ Text extras ({len(raw_text)} caractere)")
    
    # Curăță textul
    clean_text = clean_raw_text(raw_text)
    print(f"  ✓ Text curățat ({len(clean_text)} caractere)")
    
    # Segmentează întrebările
    questions = segment_questions(clean_text)
    
    if not questions:
        print("  ⚠️  Nu s-au detectat întrebări numerotate")
        return []
    
    print(f"  ✓ Detectate {len(questions)} întrebări")
    
    # Extrage șabloanele
    templates = process_raw_questions(questions)
    print(f"  ✓ Extrase {len(templates)} șabloane")
    
    # Adaugă sursa la fiecare șablon
    for tmpl in templates:
        tmpl['source_file'] = pdf_path.name
    
    return templates


def deduplicate_templates(all_templates: List[Dict]) -> List[Dict]:
    """
    Deduplică șabloanele bazat pe textul șablonului normalizat.
    
    Args:
        all_templates: Lista de șabloane de la toate PDF-urile
        
    Returns:
        Lista dedupicată de șabloane
    """
    seen_templates: Set[str] = set()
    unique_templates: List[Dict] = []
    
    for tmpl in all_templates:
        # Normalizăm pentru comparare (lowercase, spații)
        template_key = tmpl['template'].lower().strip()
        
        if template_key not in seen_templates:
            seen_templates.add(template_key)
            unique_templates.append(tmpl)
        else:
            # Șablonul este duplicat, îl omitem dar logăm
            print(f"  ⓘ  Duplicat omis: {tmpl['id']} din {tmpl.get('source_file', 'unknown')}")
    
    return unique_templates


def main_batch_extraction():
    """
    Funcție principală care procesează toate PDF-urile din assets/pdfs/examene/
    și generează un fișier master templates.json.
    """
    print("\n" + "="*60)
    print("  EXTRACȚIE BATCH - PROCESARE MULTIPLE PDF-URI")
    print("="*60)
    
    # Calea către folderul cu examene
    examene_dir = project_root.joinpath("assets", "pdfs", "examene")
    
    if not examene_dir.exists():
        print(f"\n❌ Folderul {examene_dir} nu există!")
        return
    
    # Găsește toate PDF-urile
    pdf_files = sorted(examene_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n❌ Nu s-au găsit fișiere PDF în {examene_dir}")
        return
    
    print(f"\n📄 Găsite {len(pdf_files)} fișiere PDF\n")
    
    # Procesează fiecare PDF și agregă șabloanele
    all_templates: List[Dict] = []
    
    for pdf_path in pdf_files:
        templates = process_single_pdf(pdf_path)
        all_templates.extend(templates)
    
    print(f"\n{'='*60}")
    print(f"Total șabloane extrase: {len(all_templates)}")
    print('='*60)
    
    # Deduplicare
    if all_templates:
        print("\n🔍 Deduplicare șabloane...")
        unique_templates = deduplicate_templates(all_templates)
        print(f"✓ Șabloane unice: {len(unique_templates)}")
        
        # Re-indexare ID-uri pentru consistență
        for idx, tmpl in enumerate(unique_templates, start=1):
            # Păstrăm tipul din ID-ul original (nash-X, csp-X, minmax-X)
            original_type = tmpl['id'].split('-')[0]
            tmpl['id'] = f"{original_type}-{idx}"
        
        # Salvare rezultat final
        out_dir = project_root.joinpath("assets", "json_output")
        out_dir.mkdir(parents=True, exist_ok=True)
        templates_out = out_dir.joinpath("templates.json")
        
        with open(templates_out, "w", encoding="utf-8") as tf:
            json.dump(unique_templates, tf, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Șabloane salvate în: {templates_out}")
        
        # Statistici pe categorii
        stats = {}
        for tmpl in unique_templates:
            for tag in tmpl.get('tags', []):
                stats[tag] = stats.get(tag, 0) + 1
        
        print("\n📊 Statistici pe categorii:")
        for tag, count in sorted(stats.items()):
            print(f"   {tag}: {count} șabloane")
    else:
        print("\n⚠️  Nu s-au extras șabloane din niciun PDF")
    
    print("\n" + "="*60)
    print("  EXTRACȚIE COMPLETATĂ")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Rulăm funcția principală doar când scriptul este executat direct
    main_batch_extraction()