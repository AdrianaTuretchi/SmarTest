from typing import List, Tuple

# Definim tipurile de date pentru claritate
Matrix = List[List[Tuple[int, int]]]
Coordinates = List[Tuple[int, int]]

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