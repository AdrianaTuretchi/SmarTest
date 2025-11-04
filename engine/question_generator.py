import json
import os
import random
from typing import List, Tuple, Dict, Any

# Definim tipurile de date pentru a fi mai clari
Matrix = List[List[Tuple[int, int]]]

class QuestionGenerator:
    """
    Gestionează încărcarea șabloanelor și generarea de noi întrebări.
    """
    
    def __init__(self, templates_path: str):
        """
        Inițializează generatorul prin încărcarea șabloanelor.

        Args:
            templates_path (str): Calea către fișierul templates.json.
        """
        self.templates = []
        try:
            with open(templates_path, 'r', encoding='utf-8') as f:
                all_templates = json.load(f)
            
            # Păstrăm doar șabloanele pe care știm să le gestionăm (momentan, doar 'nash')
            self.templates = {
                t['id']: t for t in all_templates 
                if t.get('tags') and 'nash' in t['tags']
            }
            
            if not self.templates:
                print(f"Atenție: Nu s-au găsit șabloane cu tag-ul 'nash' în {templates_path}")
                
        except FileNotFoundError:
            print(f"EROARE: Fișierul de șabloane nu a fost găsit la {templates_path}")
        except json.JSONDecodeError:
            print(f"EROARE: Fișierul de șabloane {templates_path} este malformat.")

    def _generate_nash_data(self) -> Matrix:
        """
        Generează o matrice de plăți aleatorie (ex: 2x2, 2x3 sau 3x2).
        """
        rows = random.randint(2, 3)
        cols = random.randint(2, 3)
        
        matrix = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                # Generează plăți cu numere mici pentru a fi ușor de citit
                p1_payoff = random.randint(0, 9)
                p2_payoff = random.randint(0, 9)
                row.append((p1_payoff, p2_payoff))
            matrix.append(row)
            
        return matrix

    def _format_matrix_as_string(self, matrix: Matrix) -> str:
        """
        Formatează matricea brută într-un string lizibil pentru a fi 
        pus în textul întrebării.
        """
        matrix_str = "\nMatricea de plăți (Jucător 1: rânduri, Jucător 2: coloane):\n"
        matrix_str += "--------------------------------------------------\n"
        
        for row in matrix:
            # Formatăm fiecare tuplu pentru a fi aliniat
            row_str = "\t".join([f"({p1},{p2})" for p1, p2 in row])
            matrix_str += f"\t{row_str}\n"
            
        matrix_str += "--------------------------------------------------\n"
        return matrix_str

    def generate_question_by_type(self, q_type: str = "nash") -> Dict[str, Any]:
        """
        Generează o întrebare completă (text + datele brute) pentru un tip dat.
        
        Returns:
            Un dicționar care conține textul final al întrebării
            și datele brute (matricea) pentru rezolvare/evaluare.
        """
        if q_type != 'nash' or not self.templates:
            return {"error": "Nu s-au găsit șabloane pentru tipul 'nash'."}
        
        # 1. Alege un șablon la întâmplare (dacă avem mai multe de tip 'nash')
        template_id = random.choice(list(self.templates.keys()))
        template_text = self.templates[template_id]['template']
        
        # 2. Generează date noi
        raw_matrix = self._generate_nash_data()
        
        # 3. Formatează datele
        formatted_matrix_str = self._format_matrix_as_string(raw_matrix)
        
        # 4. Asamblează întrebarea finală
        # Adăugăm matricea DUPĂ șablonul nostru (care se termină cu "Justificați.")
        final_question_text = template_text + "\n" + formatted_matrix_str
        
        return {
            "question_text": final_question_text,
            "raw_data": raw_matrix,  # crucial pentru pasul următor
            "template_id": template_id
        }


