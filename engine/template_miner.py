import re
from typing import List, Dict, Optional
from utils.text_cleaner import normalize_ro_diacritics


def _normalize_whitespace(s: str) -> str:
    """ Normalizează spațiile multiple într-unul singur. """
    return re.sub(r"\s+", " ", s).strip()


def _extract_generic_template(q_norm: str, q_lower: str) -> str:
    """
    Extrage partea generică a întrebării, tăind la primele date specifice.
    
    Detectează ancori comune pentru date de instanță:
    - "Matricea:", "Tabela:", "Graful:", "Variabile:", "Domenii:"
    - "Avem următoarea...", "Pentru ... de mai jos"
    """
    # Ancori pentru date specifice de instanță
    data_headers = [
        r"Matricea\s*:",
        r"Tabela\s*:",
        r"Graful\s*:",
        r"Variabile\s*:",
        r"Domenii\s*:",
        r"Avem\s+(următoarea|urmatoarea)\s+(instanț|problema)",
        r"Pentru\s+(jocul|arborele|graful)\s+(de\s+)?mai\s+jos",
        r"Pentru\s+(jocul|arborele|graful)\s+dat",
    ]
    
    # Găsim prima ancorare
    earliest_pos = len(q_norm)
    
    for pattern in data_headers:
        match = re.search(pattern, q_norm, re.IGNORECASE)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
    
    # Tăiem la prima ancorare sau păstrăm tot
    if earliest_pos < len(q_norm):
        template_text = q_norm[:earliest_pos].strip()
        # Dacă am tăiat și textul e prea scurt, păstrăm originalul
        if len(template_text) < 30:
            template_text = q_norm
    else:
        template_text = q_norm
    
    return template_text


def _classify_question(q_norm: str, q_lower: str) -> Optional[tuple]:
    """
    Clasifică întrebarea în una din cele trei categorii.
    
    Returns:
        Tuple (category_name, tags_list) sau None dacă nu se potrivește
    """
    
    # --- PATTERN 1: CSP (Constraint Satisfaction Problem) ---
    # Trigger phrases: "satisfacere restricțiilor" OR "graf constrângeri" OR 
    #                  "Forward checking" OR "Arc consistency" OR "MRV"
    csp_pattern = r"(satisfacere.*restric|graf.*constr[aă]nger|forward\s*checking|arc\s*consistency|mrv)"
    
    if re.search(csp_pattern, q_lower, re.IGNORECASE):
        return ('csp', ['csp', 'constraint-satisfaction'])
    
    # --- PATTERN 2: MinMax (Adversarial Search) ---
    # Trigger phrases: "MIN-MAX", "MINIMAX", "Alpha-Beta" (with or without dash/space)
    minmax_pattern = r"(min\s*-?\s*max|alpha\s*-?\s*beta)"
    
    if re.search(minmax_pattern, q_lower, re.IGNORECASE):
        return ('minmax', ['minmax', 'alpha-beta', 'game-tree'])
    
    # --- PATTERN 3: Nash Equilibrium (Game Theory) ---
    # Trigger phrases: "echilibru nash" OR "strategii dominate"
    nash_pattern = r"(echilibru\s*nash|strategii\s*dominat)"
    
    if re.search(nash_pattern, q_lower, re.IGNORECASE):
        return ('nash', ['nash', 'game-theory'])
    
    return None


def process_raw_questions(raw_questions: List[str]) -> List[Dict]:
    """
    Procesează o listă de întrebări brute extrase, le clasifică
    și extrage șabloanele generice pentru Nash, CSP și MinMax.
    
    Folosește pattern matching robust și flexibil pentru a detecta
    variații de frazare între diferite seturi de examene.
    
    Args:
        raw_questions: Lista de string-uri cu întrebări extrase din PDF-uri
        
    Returns:
        Lista de dicționare cu șabloane extrase:
        [
            {
                'id': 'nash-1',
                'template': 'text șablon...',
                'tags': ['nash', 'game-theory'],
                'source_text_for_debug': 'text complet original'
            },
            ...
        ]
    """
    templates = []
    
    # Contoare pentru ID-uri unice pe categorie
    counters = {'nash': 0, 'csp': 0, 'minmax': 0}
    
    for q in raw_questions:
        q_norm = _normalize_whitespace(q)
        q_lower = q_norm.lower()
        
        # Skip dacă întrebarea e prea scurtă
        if len(q_norm) < 20:
            continue
        
        # Clasificare folosind pattern matching robust
        classification = _classify_question(q_norm, q_lower)
        
        if classification is None:
            # Această întrebare nu se potrivește niciunui pattern
            continue
        
        category, tags = classification
        counters[category] += 1
        
        # Extrage șablonul generic (taie datele specifice)
        template_text = _extract_generic_template(q_norm, q_lower)
        
        # Normalizează diacriticele românești pentru a evita probleme de encoding
        template_text_clean = normalize_ro_diacritics(template_text)
        q_norm_clean = normalize_ro_diacritics(q_norm)
        
        templates.append({
            'id': f"{category}-{counters[category]}",
            'template': template_text_clean,
            'source_text_for_debug': q_norm_clean,
            'tags': tags,
        })
    
    return templates