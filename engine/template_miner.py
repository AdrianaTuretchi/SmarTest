import re
from typing import List, Dict

def _normalize_whitespace(s: str) -> str:
    """ Normalizează spațiile multiple într-unul singur. """
    return re.sub(r"\s+", " ", s).strip()

def process_raw_questions(raw_questions: List[str]) -> List[Dict]:
    """
    Procesează o listă de întrebări brute extrase, le clasifică
    și extrage șabloanele generice.
    
    Se concentrează pe extragerea corectă a șablonului Nash.
    """
    templates = []
    
    # raw_questions este lista de 6 string-uri din output-ul tău
    for i, q in enumerate(raw_questions, start=1):
        q_norm = _normalize_whitespace(q)
        q_lower = q_norm.lower()

        # --- REGULĂ PENTRU NASH EQUILIBRIUM ---
        # Căutăm cuvinte cheie specifice
        if "echilibre nash pure" in q_lower:
            
            # Am găsit întrebarea Nash. Acum extragem șablonul.
            # Șablonul se termină la "Justificați."
            # Vom tăia totul după acest cuvânt.
            
            template_text = q_norm  # Default (dacă ancora nu e găsită)
            anchor = "Justificați."
            
            # Căutăm ancora, ignorând majusculele
            match = re.search(re.escape(anchor), q_norm, re.IGNORECASE)
            
            if match:
                # Extragem totul de la început până la sfârșitul ancorei
                template_text = q_norm[:match.end()]
            
            templates.append({
                'id': f'nash-{i}',
                'template': template_text, # Acesta este acum șablonul curățat
                'source_text_for_debug': q_norm, # Păstrăm originalul pentru debug
                'tags': ['nash', 'game-theory'],
            })
            # Trecem la următoarea întrebare din buclă
            continue

        # Aici am adăuga 'elif' pentru alte tipuri de întrebări,
        # dar pentru L6 ne concentrăm doar pe Nash.
    
    return templates