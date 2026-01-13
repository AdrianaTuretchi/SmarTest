# SmarTest

Platforma de pregatire pentru examenul de Inteligenta Artificiala. Ofera generare automata de intrebari, evaluare si rezolvare automata pentru patru tipuri de probleme: Nash, CSP, MinMax si Strategy.

## Tipuri de intrebari

- **Nash** - echilibre Nash pure si strategii dominate
- **CSP** - probleme de satisfacere a restrictiilor cu Backtracking, Forward Checking, MRV
- **MinMax** - arbori de joc cu optimizare Alpha-Beta
- **Strategy** - selectarea strategiei optime pentru N-Queens, Hanoi, Graph Coloring, Knight's Tour

## Pagini

- **Home** - pagina principala cu navigare
- **Practice** - exersare libera pe categorii, intrebari generate aleator cu feedback instant
- **Test Config** - configurare test (numar intrebari per tip, timp)
- **Test Active** - rezolvarea testului cu cronometru
- **Test Results** - rezultatele testului cu scor si corectari
- **Solver** - rezolvare automata a intrebarilor din text liber

## Setup

Backend (Python):
```
git clone https://github.com/AdrianaTuretchi/SmarTest

cd SmarTest

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python -m uvicorn main:app --reload --port 8001
```

Frontend (React):
```
cd frontend

npm install

npm run dev
```

Aplicatia va fi disponibila la `http://localhost:5173`.

## Autori

Adrian Turețchi

Denis Fechet

Tudor-Emilian Miron
