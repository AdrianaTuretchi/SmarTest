"""
Question Parser Service
Detectează tipul întrebării și extrage datele pentru solveri.
"""

import re
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class ParsedQuestion:
    """Rezultatul parsing-ului unei întrebări."""
    question_type: str  # 'nash', 'csp', 'strategy', 'minmax', 'unknown'
    extracted_data: Dict[str, Any]
    confidence: float  # 0.0 - 1.0
    error_message: Optional[str] = None


class QuestionParser:
    """
    Parser pentru întrebări din domeniile: Nash, CSP, Strategy, MinMax.
    Folosește keywords și regex pentru detectare și extracție.
    """

    # Keywords pentru detectarea tipului
    NASH_KEYWORDS = [
        'nash', 'echilibru', 'echilibre', 'equilibrium', 'equilibria',
        'matrice', 'matrix', 'jucător', 'jucatori', 'player', 'players',
        'payoff', 'câștig', 'castig', 'plată', 'joc', 'game theory',
        'strategie pură', 'strategie pura', 'pure strategy',
        'dominate', 'dominat', 'dominated'
    ]
    
    # Keywords pentru detectarea cererii de strategii dominate
    DOMINATED_KEYWORDS = [
        'dominate', 'dominat', 'dominated', 'dominată', 'dominata',
        'strategii dominate', 'strategie dominată', 'strategie dominata'
    ]

    CSP_KEYWORDS = [
        'csp', 'constraint', 'constrângere', 'constrangere', 'satisfacere',
        'colorare', 'coloring', 'graf', 'graph', 'variabil', 'variable',
        'domeniu', 'domain', 'backtracking', 'arc consistency', 'ac-3', 'ac3',
        'forward checking', 'mrv', 'sudoku', 'map coloring'
    ]

    STRATEGY_KEYWORDS = [
        'strategie', 'strategy', 'algoritm', 'algorithm', 'cea mai potrivită',
        'cea mai bună', 'recomand', 'n-queens', 'n-dame', 'queens',
        'căutare', 'cautare', 'search', 'rezolvare', 'abordare',
        'hanoi', 'turnuri', 'knight', 'cal', 'cavaler'
    ]

    MINMAX_KEYWORDS = [
        'minmax', 'min-max', 'minimax', 'alpha-beta', 'alpha beta',
        'arbore', 'tree', 'maximizator', 'minimizator', 'max', 'min',
        'adâncime', 'adancime', 'depth', 'tăiere', 'taiere', 'pruning'
    ]

    def parse(self, text: str) -> ParsedQuestion:
        """
        Parsează o întrebare și returnează tipul și datele extrase.
        
        Args:
            text: Textul întrebării
            
        Returns:
            ParsedQuestion cu tipul, datele și încrederea
        """
        if not text or not text.strip():
            return ParsedQuestion(
                question_type='unknown',
                extracted_data={},
                confidence=0.0,
                error_message='Textul întrebării este gol.'
            )

        text_lower = text.lower()
        
        # Detectăm tipul
        question_type, confidence = self._detect_type(text_lower)
        
        if question_type == 'unknown':
            return ParsedQuestion(
                question_type='unknown',
                extracted_data={},
                confidence=0.0,
                error_message='Nu am putut detecta tipul întrebării. Asigură-te că întrebarea conține cuvinte cheie specifice (Nash, CSP, Strategy, etc.).'
            )

        # Extragem datele în funcție de tip
        try:
            if question_type == 'nash':
                data = self._extract_nash_data(text)
            elif question_type == 'csp':
                data = self._extract_csp_data(text)
            elif question_type == 'strategy':
                data = self._extract_strategy_data(text)
            elif question_type == 'minmax':
                data = self._extract_minmax_data(text)
            else:
                data = {}

            if not data:
                return ParsedQuestion(
                    question_type=question_type,
                    extracted_data={},
                    confidence=confidence * 0.5,
                    error_message=f'Tipul "{question_type}" detectat, dar nu am putut extrage datele. Verifică formatul întrebării.'
                )

            return ParsedQuestion(
                question_type=question_type,
                extracted_data=data,
                confidence=confidence
            )

        except Exception as e:
            return ParsedQuestion(
                question_type=question_type,
                extracted_data={},
                confidence=confidence * 0.3,
                error_message=f'Eroare la extragerea datelor: {str(e)}'
            )

    def _detect_type(self, text_lower: str) -> Tuple[str, float]:
        """
        Detectează tipul întrebării bazat pe keywords.
        
        Returns:
            Tuple (tip, încredere)
        """
        scores = {
            'nash': 0,
            'csp': 0,
            'strategy': 0,
            'minmax': 0
        }

        # Calculăm scorul pentru fiecare tip
        for kw in self.NASH_KEYWORDS:
            if kw in text_lower:
                scores['nash'] += 1

        for kw in self.CSP_KEYWORDS:
            if kw in text_lower:
                scores['csp'] += 1

        for kw in self.STRATEGY_KEYWORDS:
            if kw in text_lower:
                scores['strategy'] += 1

        for kw in self.MINMAX_KEYWORDS:
            if kw in text_lower:
                scores['minmax'] += 1

        # Găsim tipul cu scorul maxim
        max_score = max(scores.values())
        if max_score == 0:
            return 'unknown', 0.0

        best_type = max(scores, key=scores.get)
        
        # PRIORITIZARE SPECIALĂ pentru Strategy:
        # Dacă întrebarea cere explicit o strategie/abordare, este de tip Strategy
        # chiar dacă conține și keywords de CSP (graph coloring, etc.)
        strategy_explicit_phrases = [
            'care este cea mai',
            'care strategie',
            'cea mai potrivită',
            'cea mai eficientă',
            'cea mai bună',
            'ce strategie',
            'ce abordare',
            'care abordare',
            'care algoritm',
            'ce algoritm'
        ]
        
        has_explicit_strategy = any(phrase in text_lower for phrase in strategy_explicit_phrases)
        
        # Dacă are fraze explicite de strategie și scorul strategy > 0, forțăm tipul strategy
        if has_explicit_strategy and scores['strategy'] > 0:
            best_type = 'strategy'
            max_score = max(max_score, scores['strategy'] + 2)  # Bonus pentru match explicit
        
        # Calculăm încrederea (normalizată)
        total_keywords = len(self.NASH_KEYWORDS) + len(self.CSP_KEYWORDS) + \
                        len(self.STRATEGY_KEYWORDS) + len(self.MINMAX_KEYWORDS)
        confidence = min(1.0, max_score / 3)  # 3+ keywords = 100% încredere

        return best_type, confidence

    def _extract_nash_data(self, text: str) -> Dict[str, Any]:
        """
        Extrage matricea de payoff din textul întrebării Nash.
        
        Formaturi suportate:
        - (3,2) (1,4) / (2,1) (4,3)
        - [[3,2], [1,4]] sau [[(3,2), (1,4)], ...]
        - Tabel cu valori separate de spații/virgule
        """
        data = {}
        
        # Pattern pentru perechi (x,y) sau (x, y)
        pair_pattern = r'\((\d+)\s*,\s*(\d+)\)'
        
        # Încercăm să detectăm numărul de coloane pe baza primei linii cu perechi
        lines = text.split('\n')
        pairs_per_line = []
        all_pairs = []
        
        for line in lines:
            line_pairs = re.findall(pair_pattern, line)
            if line_pairs:
                pairs_per_line.append(len(line_pairs))
                all_pairs.extend(line_pairs)
        
        if all_pairs:
            # Determinăm numărul de coloane din prima linie cu perechi
            # sau din modul (cel mai frecvent număr de perechi pe linie)
            if pairs_per_line:
                # Ignorăm liniile cu un singur element (pot fi titluri)
                valid_counts = [c for c in pairs_per_line if c > 0]
                if valid_counts:
                    # Folosim primul rând valid pentru a determina coloanele
                    cols = valid_counts[0]
                    num_pairs = len(all_pairs)
                    
                    if num_pairs % cols == 0:
                        rows = num_pairs // cols
                        matrix = []
                        idx = 0
                        for r in range(rows):
                            row = []
                            for c in range(cols):
                                if idx < len(all_pairs):
                                    p1, p2 = int(all_pairs[idx][0]), int(all_pairs[idx][1])
                                    row.append([p1, p2])
                                    idx += 1
                            matrix.append(row)
                        
                        data['raw_data'] = matrix
                        data['rows'] = rows
                        data['cols'] = cols
        
        # Fallback: metoda veche dacă nu am putut detecta din linii
        if 'raw_data' not in data:
            pairs = re.findall(pair_pattern, text)
            if pairs:
                num_pairs = len(pairs)
                
                # Încercăm dimensiuni comune: prioritizăm mai multe rânduri (matrice mai înalte)
                for rows in [4, 3, 2]:
                    if num_pairs % rows == 0:
                        cols = num_pairs // rows
                        matrix = []
                        idx = 0
                        for r in range(rows):
                            row = []
                            for c in range(cols):
                                if idx < len(pairs):
                                    p1, p2 = int(pairs[idx][0]), int(pairs[idx][1])
                                    row.append([p1, p2])
                                    idx += 1
                            matrix.append(row)
                        
                        if idx == num_pairs:
                            data['raw_data'] = matrix
                            data['rows'] = rows
                            data['cols'] = cols
                            break
        
        # Alternativ: căutăm numere în format tabel
        if 'raw_data' not in data:
            # Pattern pentru numere separate
            numbers = re.findall(r'\b(\d+)\b', text)
            numbers = [int(n) for n in numbers if int(n) < 100]  # Filtrăm numere mari
            
            # Dacă avem numere pare, încercăm să formăm perechi
            if len(numbers) >= 4 and len(numbers) % 2 == 0:
                pairs = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
                num_pairs = len(pairs)
                
                for rows in [2, 3]:
                    if num_pairs % rows == 0:
                        cols = num_pairs // rows
                        matrix = []
                        idx = 0
                        for r in range(rows):
                            row = []
                            for c in range(cols):
                                if idx < len(pairs):
                                    row.append(list(pairs[idx]))
                                    idx += 1
                            matrix.append(row)
                        
                        if idx == num_pairs:
                            data['raw_data'] = matrix
                            data['rows'] = rows
                            data['cols'] = cols
                            break

        # Detectăm dacă întrebarea cere strategii dominate
        text_lower = text.lower()
        asks_dominated = any(kw in text_lower for kw in self.DOMINATED_KEYWORDS)
        data['asks_dominated'] = asks_dominated

        return data

    def _extract_csp_data(self, text: str) -> Dict[str, Any]:
        """
        Extrage variabile, domenii și constrângeri pentru CSP.
        
        Formaturi suportate:
        - Variabile: A, B, C, D sau X1, X2, X3 sau ['A', 'B', 'C']
        - Domenii: {1, 2, 3} sau [roșu, verde, albastru] sau {'A': [1,2,3], 'B': [1,2]}
        - Constrângeri: A != B, A-B, A ≠ B, muchii: A-B, B-C
        - Asignare parțială: {'E': 1}
        """
        data = {}
        text_lower = text.lower()
        
        # Detectăm variabile în format Python list: ['A', 'B', 'C']
        var_list_pattern = r"[Vv]ariabile\s*[:\-]?\s*\[([^\]]+)\]"
        var_list_match = re.search(var_list_pattern, text)
        if var_list_match:
            # Extragem variabilele din lista Python
            var_str = var_list_match.group(1)
            variables = re.findall(r"'([A-Za-z]\d*)'|\"([A-Za-z]\d*)\"", var_str)
            variables = [v[0] or v[1] for v in variables if v[0] or v[1]]
            variables = [v.upper() for v in variables]
        else:
            # Detectăm variabile (litere mari singulare sau Xn)
            var_pattern = r'\b([A-Z])\b(?!\w)|([Xx]\d+)'
            var_matches = re.findall(var_pattern, text)
            variables = list(set([m[0] or m[1].upper() for m in var_matches if m[0] or m[1]]))
            variables = sorted(variables)
        
        # Dacă nu găsim variabile, căutăm în format "Noduri: A, B, C"
        if not variables:
            nodes_pattern = r'[Nn]oduri\s*[:\-]?\s*([A-Za-z,\s]+)'
            nodes_match = re.search(nodes_pattern, text)
            if nodes_match:
                variables = [v.strip().upper() for v in nodes_match.group(1).split(',') if v.strip()]
        
        if variables:
            data['variables'] = variables
        
        # Detectăm domeniile în format Python dict: {'A': [1, 2, 3], 'B': [1, 2]}
        domains_dict_pattern = r"[Dd]omenii\s*[:\-]?\s*\{([^\}]+(?:\[[^\]]*\][^\}]*)+)\}"
        domains_match = re.search(domains_dict_pattern, text)
        
        if domains_match:
            domains_str = domains_match.group(1)
            # Parsăm fiecare variabilă și domeniul său: 'A': [1, 2, 3]
            domain_items = re.findall(r"'([A-Za-z]\d*)'\s*:\s*\[([^\]]+)\]", domains_str)
            domains = {}
            for var, vals in domain_items:
                var = var.upper()
                values = [int(v.strip()) for v in vals.split(',') if v.strip().isdigit()]
                domains[var] = values
            if domains:
                data['domains'] = domains
        else:
            # Format: A ∈ {1, 2}, B ∈ {1, 2, 3} sau A in {1, 2}
            individual_domain_pattern = r'([A-Z])\s*(?:∈|in|∊)\s*\{([^}]+)\}'
            individual_matches = re.findall(individual_domain_pattern, text, re.IGNORECASE)
            
            if individual_matches:
                domains = {}
                for var, vals in individual_matches:
                    var = var.upper()
                    values = [int(v.strip()) for v in re.findall(r'\d+', vals)]
                    if values:
                        domains[var] = values
                if domains:
                    data['domains'] = domains
            else:
                # Pattern vechi: domeniu {1, 2, 3} sau 3 culori
                domain_pattern = r'(\d+)\s*culor|domeniu\s*[:\{]?\s*[\{\[]?([^\}\]]+)[\}\]]?'
                domain_match = re.search(domain_pattern, text_lower)
                
                if domain_match:
                    if domain_match.group(1):  # N culori
                        n_colors = int(domain_match.group(1))
                        data['domain_size'] = n_colors
                        data['domains'] = {v: list(range(1, n_colors + 1)) for v in variables}
                    elif domain_match.group(2):
                        domain_values = re.findall(r'\d+', domain_match.group(2))
                        if domain_values:
                            domain = [int(d) for d in domain_values]
                            data['domains'] = {v: domain for v in variables}
                else:
                    # Default: 3 culori dacă e problemă de colorare
                    if 'color' in text_lower or 'culor' in text_lower:
                        data['domain_size'] = 3
                        data['domains'] = {v: [1, 2, 3] for v in variables}
        
        # Detectăm constrângeri (muchii) - suportăm și simbolul ≠
        # Pattern: A-B, A!=B, A ≠ B, muchii: A-B, B-C
        edge_pattern = r'([A-Z])\s*[-–—]\s*([A-Z])|([A-Z])\s*[!≠]=?\s*([A-Z])'
        edge_matches = re.findall(edge_pattern, text)
        constraints = []
        for m in edge_matches:
            if m[0] and m[1]:
                constraints.append([m[0], m[1]])
            elif m[2] and m[3]:
                constraints.append([m[2], m[3]])
        
        # Căutăm și în format "Constrângeri: A ≠ B, B ≠ C"
        constr_pattern = r"[Cc]onstrângeri\s*[:\-]?\s*(.+?)(?:\n|$)"
        constr_match = re.search(constr_pattern, text)
        if constr_match:
            constr_text = constr_match.group(1)
            # Extragem perechi din text
            pairs = re.findall(r'([A-Z])\s*[≠!=]+\s*([A-Z])', constr_text)
            for p1, p2 in pairs:
                if [p1, p2] not in constraints and [p2, p1] not in constraints:
                    constraints.append([p1, p2])
        
        # Eliminăm duplicate
        unique_constraints = []
        seen = set()
        for c in constraints:
            key = tuple(sorted(c))
            if key not in seen:
                seen.add(key)
                unique_constraints.append(list(c))
        
        if unique_constraints:
            data['constraints'] = unique_constraints
        
        # Detectăm asignarea parțială: {'E': 1} sau Asignare parțială: {'E': 1}
        partial_pattern = r"[Aa]signare\s*par[țt]ial[aă]\s*[:\-]?\s*\{([^\}]+)\}"
        partial_match = re.search(partial_pattern, text)
        if partial_match:
            partial_str = partial_match.group(1)
            # Parsăm: 'E': 1
            partial_items = re.findall(r"'([A-Za-z]\d*)'\s*:\s*(\d+)", partial_str)
            partial_assignment = {}
            for var, val in partial_items:
                partial_assignment[var.upper()] = int(val)
            if partial_assignment:
                data['partial_assignment'] = partial_assignment

        # Adăugăm tags pentru tipul de problemă
        data['tags'] = []
        if 'color' in text_lower or 'culor' in text_lower:
            data['tags'].append('graph-coloring')
        if 'sudoku' in text_lower:
            data['tags'].append('sudoku')

        # Detectăm algoritmii și euristicile cerute
        # MRV (Minimum Remaining Values)
        use_mrv = any(kw in text_lower for kw in ['mrv', 'minimum remaining values', 'minimum remaining'])
        data['use_mrv'] = use_mrv
        
        # Forward Checking
        use_fc = any(kw in text_lower for kw in ['forward checking', 'forward-checking', 'fc ', ' fc,', ' fc.'])
        data['use_fc'] = use_fc
        
        # AC-3 (Arc Consistency)
        use_ac3 = any(kw in text_lower for kw in ['ac-3', 'ac3', 'arc consistency', 'arc-consistency'])
        data['use_ac3'] = use_ac3
        
        # Backtracking (aproape întotdeauna prezent)
        use_backtracking = 'backtracking' in text_lower or 'back-tracking' in text_lower
        data['use_backtracking'] = use_backtracking

        return data

    def _extract_strategy_data(self, text: str) -> Dict[str, Any]:
        """
        Extrage tipul problemei și parametrii pentru Strategy.
        
        Detectează:
        - Tip problemă: N-Queens, Graph Coloring, etc.
        - Parametri: N (dimensiune), is_tree, etc.
        """
        data = {}
        text_lower = text.lower()

        # Detectăm tipul problemei
        if 'n-queen' in text_lower or 'n queen' in text_lower or 'dame' in text_lower or 'queens' in text_lower:
            data['problem_type'] = 'n-queens'
            
            # Extragem N
            n_pattern = r'[Nn]\s*[=:]\s*(\d+)|(\d+)\s*[-–]?\s*(?:queens?|dame)'
            n_match = re.search(n_pattern, text)
            if n_match:
                n = n_match.group(1) or n_match.group(2)
                data['n'] = int(n)
            else:
                # Căutăm orice număr mare
                numbers = re.findall(r'\b(\d+)\b', text)
                large_numbers = [int(n) for n in numbers if int(n) > 3]
                if large_numbers:
                    data['n'] = large_numbers[0]

        elif 'color' in text_lower or 'culor' in text_lower or 'graf' in text_lower:
            data['problem_type'] = 'graph-coloring'
            
            # Verificăm dacă e arbore
            if 'arbore' in text_lower or 'tree' in text_lower:
                data['is_tree'] = True
            else:
                data['is_tree'] = False
            
            # Extragem numărul de noduri
            nodes_pattern = r'(\d+)\s*(?:noduri|nodes|vârfuri|varfuri)'
            nodes_match = re.search(nodes_pattern, text_lower)
            if nodes_match:
                data['num_nodes'] = int(nodes_match.group(1))

        elif 'knight' in text_lower or 'cal' in text_lower or 'cavaler' in text_lower or 'tura' in text_lower:
            data['problem_type'] = 'knight-tour'
            
            # Extragem dimensiunea tablei
            size_pattern = r'(\d+)\s*[xX×]\s*(\d+)'
            size_match = re.search(size_pattern, text)
            if size_match:
                data['board_size'] = int(size_match.group(1))
            
            # Detectăm tipul obiectivului
            if 'rapid' in text_lower or 'fast' in text_lower or 'greedy' in text_lower or 'eficient' in text_lower:
                data['goal_type'] = 'fast'
            elif 'complet' in text_lower or 'toate' in text_lower or 'backtrack' in text_lower:
                data['goal_type'] = 'complete'
            else:
                data['goal_type'] = 'fast'  # default pentru "găsirea rapidă"

        elif 'hanoi' in text_lower or 'turnuri' in text_lower:
            data['problem_type'] = 'hanoi'
            
            # Extragem numărul de discuri
            disc_pattern = r'(\d+)\s*(?:discuri|disc|disks?)'
            disc_match = re.search(disc_pattern, text_lower)
            if disc_match:
                data['num_discs'] = int(disc_match.group(1))
            
            # Detectăm tipul obiectivului
            # "fără restricție de optim", "oricărei soluții" = any solution
            if 'fără restricție' in text_lower or 'fara restrictie' in text_lower or 'oricare' in text_lower or 'oricărei' in text_lower:
                data['goal_type'] = 'any'
            elif 'optim' in text_lower or 'minim' in text_lower or 'cel mai scurt' in text_lower:
                data['goal_type'] = 'optimal'
            else:
                data['goal_type'] = 'any'

        elif 'sudoku' in text_lower:
            data['problem_type'] = 'sudoku'
            
        elif 'scheduling' in text_lower or 'planificare' in text_lower:
            data['problem_type'] = 'scheduling'

        # Adăugăm tags
        data['tags'] = ['strategy']
        if data.get('problem_type'):
            data['tags'].append(data['problem_type'])

        return data

    def _extract_minmax_data(self, text: str) -> Dict[str, Any]:
        """
        Extrage arborele MinMax din text.
        
        Suportă formatul ASCII tree generat de aplicație:
        └── [ ]
            └── [ ]
                └── 11
                ┌── 3
            ┌── [ ]
                └── 3
                ┌── 6
        """
        data = {'tags': ['minmax']}
        
        # Căutăm linii care conțin noduri (└── sau ┌──)
        lines = text.split('\n')
        tree_lines = []
        
        for line in lines:
            # Detectăm linii care fac parte din arbore
            if '└──' in line or '┌──' in line:
                tree_lines.append(line)
        
        if not tree_lines:
            # Încercăm alt format - numere pe linii separate (frunze)
            # sau format cu paranteze
            return self._extract_minmax_from_numbers(text)
        
        # Parsăm arborele din liniile găsite
        try:
            tree = self._parse_ascii_tree(tree_lines)
            if tree:
                data['raw_data'] = tree
                data['tree_depth'] = self._get_tree_depth(tree)
        except Exception as e:
            data['parse_error'] = str(e)
        
        return data
    
    def _parse_ascii_tree(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parsează arborele ASCII și returnează structura dict.
        """
        if not lines:
            return None
        
        def get_indent_level(line: str) -> int:
            """Calculează nivelul de indentare (4 spații = 1 nivel)"""
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            return indent // 4
        
        def parse_node_value(line: str):
            """Extrage valoarea nodului din linie"""
            # Căutăm [ ] pentru noduri interne sau numere pentru frunze
            if '[ ]' in line:
                return None  # Nod intern
            # Căutăm un număr
            match = re.search(r'[└┌]──\s*(\d+)', line)
            if match:
                return int(match.group(1))
            return None
        
        # Construim arborele recursiv
        def build_tree(start_idx: int, parent_indent: int) -> Tuple[Dict[str, Any], int]:
            if start_idx >= len(lines):
                return None, start_idx
            
            line = lines[start_idx]
            indent = get_indent_level(line)
            value = parse_node_value(line)
            
            node = {
                "value": value,
                "children": []
            }
            
            next_idx = start_idx + 1
            
            # Dacă e nod intern (value=None), căutăm copiii
            if value is None:
                # Căutăm copiii - sunt la indent + 1
                while next_idx < len(lines):
                    child_indent = get_indent_level(lines[next_idx])
                    
                    if child_indent <= indent:
                        # Am ieșit din sub-arbore
                        break
                    
                    if child_indent == indent + 1:
                        # E un copil direct
                        child_node, next_idx = build_tree(next_idx, indent + 1)
                        if child_node:
                            node["children"].append(child_node)
                    else:
                        next_idx += 1
            
            return node, next_idx
        
        tree, _ = build_tree(0, -1)
        return tree
    
    def _extract_minmax_from_numbers(self, text: str) -> Dict[str, Any]:
        """
        Extrage arborele MinMax din numere pentru cazuri simple.
        Format: frunzele arborelui sunt listate ca numere.
        """
        data = {'tags': ['minmax']}
        
        # Căutăm numere care ar putea fi frunze
        # Pattern: secvențe de numere separate
        numbers = re.findall(r'\b(\d{1,2})\b', text)
        leaf_values = [int(n) for n in numbers if 0 <= int(n) <= 99]
        
        # Trebuie să fie putere de 2 pentru un arbore binar complet
        if len(leaf_values) >= 2:
            # Găsim cea mai apropiată putere de 2
            power = 1
            while power < len(leaf_values):
                power *= 2
            
            # Luăm primele 'power' frunze sau completăm
            if len(leaf_values) >= power // 2:
                leaf_values = leaf_values[:power] if len(leaf_values) >= power else leaf_values[:power // 2 * 2]
            
            if len(leaf_values) >= 2 and (len(leaf_values) & (len(leaf_values) - 1)) == 0:
                # E putere de 2, construim arborele
                tree = self._build_tree_from_leaves(leaf_values)
                if tree:
                    data['raw_data'] = tree
                    data['leaf_values'] = leaf_values
                    data['tree_depth'] = self._get_tree_depth(tree)
        
        return data
    
    def _build_tree_from_leaves(self, leaves: List[int]) -> Dict[str, Any]:
        """
        Construiește un arbore binar complet din valorile frunzelor.
        """
        if len(leaves) == 1:
            return {"value": leaves[0], "children": []}
        
        # Împărțim în două și construim recursiv
        mid = len(leaves) // 2
        left_subtree = self._build_tree_from_leaves(leaves[:mid])
        right_subtree = self._build_tree_from_leaves(leaves[mid:])
        
        return {
            "value": None,
            "children": [left_subtree, right_subtree]
        }
    
    def _get_tree_depth(self, tree: Dict[str, Any]) -> int:
        """Calculează adâncimea arborelui."""
        if not tree or not tree.get("children"):
            return 0
        return 1 + max(self._get_tree_depth(c) for c in tree["children"])
