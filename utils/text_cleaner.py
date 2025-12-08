import re
from collections import Counter
from typing import List


def clean_raw_text(text: str) -> str:
    """
    Curata textul brut extras din PDF.

    Passurile facute:
    - Elimina BOM-uri si caractere non-breaking.
    - Reparare ligaturi comune (ﬁ -> fi, ﬀ -> ff, etc.).
    - Uneste cuvintele silabizate la cap de linie (hyphenation): "exam-\nple" -> "example".
    - Normalizare newline-uri si reducere spatii multiple.
    - Scoate linii care par a fi numere de pagina sau linii foarte scurte/numere.
    - Detecteaza linii scurte repetate (probabile header/footer) si le elimina.

    Args:
        text: textul brut extras din PDF

    Returns:
        textul curatat
    """
    if not text:
        return text

    # 1) Normalize newline and remove BOM / NBSP
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.replace('\ufeff', '').replace('\xa0', ' ')

    # 2) Fix common ligatures
    ligatures = {
        '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl',
        'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', 'ﬀ': 'ff'
    }
    for k, v in ligatures.items():
        text = text.replace(k, v)

    # 3) Split into lines and handle hyphenation at line endings
    lines = [ln.rstrip() for ln in text.split('\n')]
    joined_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # If line ends with a hyphenated word, join with next line without the hyphen
        if line.endswith('-') and i + 1 < len(lines):
            next_line = lines[i + 1].lstrip()
            # remove the trailing hyphen and concatenate directly
            line = line[:-1] + next_line
            i += 1  # consume next line as well
        joined_lines.append(line)
        i += 1

    # 4) Remove obvious page numbers and very short numeric lines
    filtered_lines = []
    num_pattern = re.compile(r'^\s*(?:Page\s*)?\d+\s*$|^\s*[-–—]\s*$')
    for ln in joined_lines:
        if num_pattern.match(ln):
            continue
        filtered_lines.append(ln)

    # 5) Detect repeated short lines (possible headers/footers) and remove them
    # Consider lines shorter than 120 chars and count frequency
    short_lines = [ln for ln in filtered_lines if 0 < len(ln) <= 120]
    counts = Counter(short_lines)
    # Remove lines that appear more than 2 times (heuristic)
    to_remove = {ln for ln, c in counts.items() if c > 2}
    cleaned_lines = [ln for ln in filtered_lines if ln not in to_remove]

    # 6) Reconstruct text but preserve paragraph breaks: replace single newlines inside paragraphs with space
    paragraphs = []
    buffer = []
    for ln in cleaned_lines:
        if ln.strip() == '':
            if buffer:
                paragraphs.append(' '.join(buffer).strip())
                buffer = []
        else:
            buffer.append(re.sub(r'\s+', ' ', ln))
    if buffer:
        paragraphs.append(' '.join(buffer).strip())

    cleaned = '\n\n'.join(paragraphs)

    # 7) Collapse more than 2 newlines and trim
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()

    return cleaned


def segment_questions(cleaned_text: str) -> List[str]:
    """
    Sparge textul curățat într-o listă de întrebări individuale.
    Folosește ca separator principal numerele de la începutul întrebărilor (ex: 1., 2., 3.).

    Args:
        cleaned_text: Textul care a trecut deja prin 'clean_raw_text'.

    Returns:
        O listă de string-uri, unde fiecare string este o întrebare.
    """

    if not cleaned_text:
        return []

    # More flexible pattern: split at any position where (possibly after whitespace)
    # a numbered item starts (e.g. "1.", "2."). This allows detection when the
    # numbering is on the same paragraph (e.g. "Student/An/Grupa: 1.").
    pattern = r"(?=\s*\d+\.)"

    potential_questions = re.split(pattern, cleaned_text)

    cleaned_questions: List[str] = []
    for q in potential_questions:
        q_stripped = q.strip()

        # Ignorăm orice bucăți goale
        if not q_stripped:
            continue

        # Păstrăm doar bucățile care încep cu un număr urmat de punct
        if re.match(r"^\d+\.", q_stripped):
            cleaned_questions.append(q_stripped)

    return cleaned_questions


def normalize_ro_diacritics(text: str) -> str:
    """
    Normalizează diacriticele românești înlocuindu-le cu echivalente ASCII.
    
    Acest lucru rezolvă problemele de encoding vizual cauzate de caractere speciale.
    
    Args:
        text: textul cu diacritice românești
        
    Returns:
        textul cu caractere ASCII normalizate
    """
    diacritics_map = {
        'ă': 'a', 'Ă': 'A',
        'â': 'a', 'Â': 'A',
        'î': 'i', 'Î': 'I',
        'ș': 's', 'Ș': 'S', 'ş': 's', 'Ş': 'S',
        'ț': 't', 'Ț': 'T', 'ţ': 't', 'Ţ': 'T'
    }
    
    for diacritic, replacement in diacritics_map.items():
        text = text.replace(diacritic, replacement)
    
    return text