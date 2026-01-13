from typing import List, Tuple, Dict

# Definim tipurile de date pentru claritate
Matrix = List[List[Tuple[int, int]]]
Coordinates = List[Tuple[int, int]]


def find_dominated_strategies(payoff_matrix: Matrix) -> Dict[str, List[int]]:
    """
    Găsește toate strategiile strict dominate pentru fiecare jucător.
    
    O strategie este STRICT DOMINATĂ dacă există o altă strategie care dă
    un payoff STRICT mai mare pentru TOATE strategiile posibile ale oponentului.
    
    Args:
        payoff_matrix: Matricea de plăți (lista de liste de tuple [p1, p2])
    
    Returns:
        Dict cu cheile 'player1' și 'player2', fiecare conținând lista de 
        indici ai strategiilor dominate (0-indexed)
        
    Exemplu:
        Pentru matricea unde rândul 0 este dominat de rândul 1:
        {'player1': [0], 'player2': []}
    """
    if not payoff_matrix or not payoff_matrix[0]:
        return {'player1': [], 'player2': []}
    
    num_rows = len(payoff_matrix)
    num_cols = len(payoff_matrix[0])
    
    dominated_p1 = []  # Strategii dominate pentru jucătorul 1 (rânduri)
    dominated_p2 = []  # Strategii dominate pentru jucătorul 2 (coloane)
    
    # Verificăm strategiile jucătorului 1 (rânduri)
    # Strategia i este dominată de strategia j dacă:
    # payoff_p1[j][c] > payoff_p1[i][c] pentru TOATE coloanele c
    for i in range(num_rows):
        for j in range(num_rows):
            if i == j:
                continue
            # Verificăm dacă rândul j domină strict rândul i
            is_dominated = True
            for c in range(num_cols):
                if payoff_matrix[j][c][0] <= payoff_matrix[i][c][0]:
                    is_dominated = False
                    break
            if is_dominated:
                if i not in dominated_p1:
                    dominated_p1.append(i)
                break  # Am găsit că i este dominat, nu mai căutăm
    
    # Verificăm strategiile jucătorului 2 (coloane)
    # Strategia i este dominată de strategia j dacă:
    # payoff_p2[r][j] > payoff_p2[r][i] pentru TOATE rândurile r
    for i in range(num_cols):
        for j in range(num_cols):
            if i == j:
                continue
            # Verificăm dacă coloana j domină strict coloana i
            is_dominated = True
            for r in range(num_rows):
                if payoff_matrix[r][j][1] <= payoff_matrix[r][i][1]:
                    is_dominated = False
                    break
            if is_dominated:
                if i not in dominated_p2:
                    dominated_p2.append(i)
                break  # Am găsit că i este dominat, nu mai căutăm
    
    return {
        'player1': sorted(dominated_p1),
        'player2': sorted(dominated_p2)
    }


def find_pure_nash(payoff_matrix: Matrix) -> Coordinates:
    """
    Găsește toate echilibrele Nash în strategie pură dintr-o matrice de plăți.

    Args:
        payoff_matrix: O listă de liste de tuple. 
                       Ex: [[(1, 2), (0, 5)], [(3, 1), (2, 0)]]
                       (Jucătorul 1 alege rândul, Jucătorul 2 alege coloana)

    Returns:
        O listă de tuple (rând, coloană) reprezentând coordonatele 
        tuturor echilibrelor Nash pure.
    """
    
    if not payoff_matrix or not payoff_matrix[0]:
        return []

    num_rows = len(payoff_matrix)
    num_cols = len(payoff_matrix[0])
    
    equilibria = []

    # Iterăm prin fiecare celulă (r, c) din matrice
    for r in range(num_rows):
        for c in range(num_cols):
            payoff_p1, payoff_p2 = payoff_matrix[r][c]
            
            # --- Verificare pentru Jucătorul 1 (Rânduri) ---
            # Este P1 mulțumit de alegerea sa (rândul 'r')?
            # Verificăm dacă P1 ar câștiga mai mult mutându-se pe alt rând,
            # în timp ce P2 RĂMÂNE pe coloana 'c'.
            is_p1_best_response = True
            for i in range(num_rows):
                if payoff_matrix[i][c][0] > payoff_p1:
                    is_p1_best_response = False
                    break # P1 are o mutare mai bună, deci (r, c) nu e echilibru
            
            # Dacă P1 nu e mulțumit, trecem la următoarea celulă
            if not is_p1_best_response:
                continue

            # --- Verificare pentru Jucătorul 2 (Coloane) ---
            # Este P2 mulțumit de alegerea sa (coloana 'c')?
            # Verificăm dacă P2 ar câștiga mai mult mutându-se pe altă coloană,
            # în timp ce P1 RĂMÂNE pe rândul 'r'.
            is_p2_best_response = True
            for j in range(num_cols):
                if payoff_matrix[r][j][1] > payoff_p2:
                    is_p2_best_response = False
                    break # P2 are o mutare mai bună, deci (r, c) nu e echilibru
            
            # Dacă AMBII jucători sunt mulțumiți (nu au niciun stimulent
            # să își schimbe unilateral strategia), am găsit un echilibru Nash.
            if is_p2_best_response:
                equilibria.append((r, c))

    return equilibria