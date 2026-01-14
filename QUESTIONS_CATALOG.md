# Catalogul Intrebarilor SmarTest

Total: 51 intrebari
- NASH: 10
- CSP: 10
- MINMAX: 10
- STRATEGY: 21

---

## 1. NASH

```
Pentru jocul de mai jos (reprezentat prin matricea de plati), identificati toate echilibrele Nash pure (daca exista).

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(3,5)	(7,2)
	(1,4)	(6,8)
--------------------------------------------------

Raspuns: (0, 0)

```

```
Pentru jocul de mai jos (reprezentat prin matricea de plati), identificati toate echilibrele Nash pure (daca exista).

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(2,1)	(5,4)	(3,6)
	(8,2)	(4,7)	(9,1)
--------------------------------------------------

Raspuns: Nu există echilibre Nash pure.

```

```
Pentru jocul de mai jos (reprezentat prin matricea de plati), identificati toate echilibrele Nash pure (daca exista).

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(1,9)	(4,3)
	(6,5)	(2,8)
	(7,1)	(3,6)
--------------------------------------------------

Raspuns: Nu există echilibre Nash pure.

```

```
Pentru jocul de mai jos (reprezentat prin matricea de plati), identificati toate echilibrele Nash pure (daca exista).

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(4,2)	(1,7)	(5,3)
	(8,1)	(3,9)	(6,4)
	(2,5)	(9,2)	(7,8)
--------------------------------------------------

Raspuns: (2, 2)

```

```
Pentru jocul de mai jos (reprezentat prin matricea de plati), identificati toate echilibrele Nash pure (daca exista).

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(0,0)	(1,1)
	(2,2)	(0,3)
--------------------------------------------------

Raspuns: (0, 1)

```

```
Pentru jocul de mai jos exista strategii dominate pentru cel putin unul din cei doi jucatori? Dar echilibre Nash pure?

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(3,1)	(2,3)	(1,4)
	(1,1)	(4,2)	(1,4)
--------------------------------------------------

Raspuns: 

Strategii Dominate:
Jucător 2 (coloane):
S1 (col 0)
S2 (col 1)

Echilibre Nash găsite:
(0, 2)
(1, 2)

```

```
Pentru jocul de mai jos exista strategii dominate pentru cel putin unul din cei doi jucatori? Dar echilibre Nash pure?

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(5,5)	(0,6)
	(6,0)	(1,1)
--------------------------------------------------

Raspuns:

Strategii Dominate:
Jucător 1 (rânduri):
S1 (rând 0)
Jucător 2 (coloane):
S1 (col 0)
Echilibre Nash găsite:
(1, 1)

```

```
Pentru jocul de mai jos exista strategii dominate pentru cel putin unul din cei doi jucatori? Dar echilibre Nash pure?

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(2,2)	(4,1)	(1,3)
	(1,4)	(3,3)	(2,2)
	(3,1)	(2,4)	(4,1)
--------------------------------------------------

Raspuns:

Strategii Dominate:
Nu există strategii strict dominate în această matrice.

Echilibre Nash găsite:
Nu există echilibre Nash pure.

```

```
Pentru jocul de mai jos exista strategii dominate pentru cel putin unul din cei doi jucatori? Dar echilibre Nash pure?

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(2,1)	(1,2)
	(1,2)	(2,1)
--------------------------------------------------

Raspuns:

Strategii Dominate:
Nu există strategii strict dominate în această matrice.

Echilibre Nash găsite:
Nu există echilibre Nash pure.

```

```
Pentru jocul de mai jos exista strategii dominate pentru cel putin unul din cei doi jucatori? Dar echilibre Nash pure?

Matricea de plati (Jucator 1: randuri, Jucator 2: coloane):
--------------------------------------------------
	(7,3)	(2,8)	(5,5)
	(4,6)	(6,4)	(3,7)
--------------------------------------------------

Raspuns:

Strategii Dominate:
Jucător 2 (coloane):
S1 (col 0)
Echilibre Nash găsite:
Nu există echilibre Nash pure.

```

## 2. CSP

```
Consideram o problema de satisfacere a restrictiilor definita de variabilele si domeniile de mai jos. Aplicati algoritmul Backtracking + Forward checking + MRV (Minimum remaining values) pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C']
Domenii: {'A': [1, 2], 'B': [1, 2, 3], 'C': [1, 2]}
Constrangeri: A != B, B != C
Asignare partiala: {'A': 1}

Raspuns: 
A = 1
C = 1
B = 2

```

```
Consideram o problema de satisfacere a restrictiilor definita de variabilele si domeniile de mai jos. Aplicati algoritmul Backtracking + Forward checking + MRV (Minimum remaining values) pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C', 'D']
Domenii: {'A': [1, 2, 3], 'B': [1, 2], 'C': [1, 2, 3], 'D': [1, 2]}
Constrangeri: A != B, B != C, C != D, A != D
Asignare partiala: {'B': 2}

Raspuns:
B = 2
D = 1
A = 3
C = 3

```

```
Consideram o problema de satisfacere a restrictiilor definita de variabilele si domeniile de mai jos. Aplicati algoritmul Backtracking + Forward checking + MRV (Minimum remaining values) pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C', 'D', 'E']
Domenii: {'A': [1, 2], 'B': [1, 2, 3], 'C': [1, 2], 'D': [1, 2, 3], 'E': [1, 2]}
Constrangeri: A != B, B != C, C != D, D != E
Asignare partiala: {'C': 1}

Raspuns:
C = 1
A = 1
B = 2
E = 1
D = 2

```

```
Consideram o problema de satisfacere a restrictiilor definita de variabilele si domeniile de mai jos. Aplicati algoritmul Backtracking + Forward checking + MRV (Minimum remaining values) pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C']
Domenii: {'A': [1, 2, 3], 'B': [1, 2, 3], 'C': [1, 2, 3]}
Constrangeri: A != B, B != C, A != C
Asignare partiala: {'A': 2}

Raspuns:
A = 2
B = 1
C = 3

```

```
Consideram o problema de satisfacere a restrictiilor definita de variabilele si domeniile de mai jos. Aplicati algoritmul Backtracking + Forward checking + MRV (Minimum remaining values) pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C']
Domenii: {'A': [1], 'B': [1, 2], 'C': [1]}
Constrangeri: A != B, B != C, A != C
Asignare partiala: {'A': 1}

Raspuns:

Soluție găsită:
Problema nu are soluție

```

```
Consideram o problema CSP cu variabilele si domeniile specificate mai jos. Considerand asignarea partiala data, aplicati algoritmul Forward checking pentru a identifica o solutie sau inconsistenta.

Variabile: ['Q1', 'Q2', 'Q3', 'Q4']
Domenii: {'Q1': [1, 2, 3, 4], 'Q2': [1, 2, 3, 4], 'Q3': [1, 2, 3, 4], 'Q4': [1, 2, 3, 4]}
Constrangeri: Q1 != Q2, Q2 != Q3, Q3 != Q4
Asignare partiala: {'Q1': 2}

Raspuns:
Q1 = 2
Q2 = 1
Q3 = 1
Q4 = 1
```

```
Consideram o problema CSP cu variabilele si domeniile specificate mai jos. Considerand asignarea partiala data, aplicati algoritmul Forward checking pentru a identifica o solutie sau inconsistenta.

Variabile: ['A', 'B', 'C', 'D']
Domenii: {'A': [1, 2], 'B': [1, 2, 3], 'C': [1, 2], 'D': [1, 2, 3]}
Constrangeri: A != B, B != C, C != D
Asignare partiala: {'D': 3}

Raspuns:
D = 3
A = 1
B = 2
C = 1

```

```
Consideram o problema CSP definita de datele de mai jos. Utilizati euristica MRV si algoritmul FC pentru a identifica o solutie sau inconsistenta. Precizati complexitatea algoritmului.

Variabile: ['A', 'B', 'C', 'D']
Domenii: {'A': [1, 2, 3], 'B': [1, 2, 3], 'C': [1, 2, 3], 'D': [1, 2, 3]}
Constrangeri: A != B, B != C, C != D, A != D, B != D
Asignare partiala: {}

Raspuns:
A = 1
B = 2
D = 3
C = 1

```

```
Consideram o problema CSP definita de datele de mai jos. Utilizati euristica MRV si algoritmul FC pentru a identifica o solutie sau inconsistenta. Precizati complexitatea algoritmului.

Variabile: ['A', 'B', 'C', 'D', 'E']
Domenii: {'A': [1, 2], 'B': [1, 2], 'C': [1, 2], 'D': [1, 2], 'E': [1, 2]}
Constrangeri: A != B, B != C, C != D, D != E, A != E
Asignare partiala: {'A': 1}

Raspuns:
Soluție găsită:
Problema nu are soluție.

```

```
Date fiind variabilele si restrictiile de mai jos, aplicati algoritmul Arc consistency pentru a actualiza valorile variabilelor. Specificati daca problema este inconsistenta.

Variabile: ['X', 'Y', 'Z']
Domenii: {'X': [1, 2, 3], 'Y': [2, 3, 4], 'Z': [1, 2]}
Constrangeri: X != Y, Y != Z, X < Z
Asignare partiala: {}

Raspuns:
Z = 1
X = 1
Y = 2
```

## 3. MINMAX

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 3
        ┌── 5
    ┌── [ ]
        └── 12
        ┌── 8

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
8
Noduri frunză vizitate:
4
Ordinea vizitării:
3
5
12
8

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 7
        ┌── 2
    ┌── [ ]
        └── 9
        ┌── 4

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
4
Noduri frunză vizitate:
4
Ordinea vizitării:
7
2
9
4

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── [ ]
            └── 3
            ┌── 5
        ┌── [ ]
            └── 6
            ┌── 9
    ┌── [ ]
        └── [ ]
            └── 1
            ┌── 2
        ┌── [ ]
            └── 0
            ┌── 4

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
5
Noduri frunză vizitate:
5
Ordinea vizitării:
3
5
6
1
2

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── [ ]
            └── 15
            ┌── 8
        ┌── [ ]
            └── 12
            ┌── 20
    ┌── [ ]
        └── [ ]
            └── 5
            ┌── 18
        ┌── [ ]
            └── 11
            ┌── 7

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
15
Noduri frunză vizitate:
8
Ordinea vizitării:
15
8
12
20
5
18
11
7

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 1
        ┌── 9
    ┌── [ ]
        └── 2
        ┌── 6

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
2
Noduri frunză vizitate:
4
Ordinea vizitării:
1
9
2
6

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── [ ]
            └── [ ]
                └── 3
                ┌── 17
            ┌── [ ]
                └── 2
                ┌── 12
        ┌── [ ]
            └── [ ]
                └── 15
                ┌── 25
            ┌── [ ]
                └── 6
                ┌── 14
    ┌── [ ]
        └── [ ]
            └── [ ]
                └── 8
                ┌── 4
            ┌── [ ]
                └── 16
                ┌── 11
        ┌── [ ]
            └── [ ]
                └── 7
                ┌── 19
            ┌── [ ]
                └── 9
                ┌── 13

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
9
Noduri frunză vizitate:
13
Ordinea vizitării:
3
17
2
15
25
8
4
16
11
7
19
9
13

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 10
        ┌── 5
    ┌── [ ]
        └── 7
        ┌── 3

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
5
Noduri frunză vizitate:
4
Ordinea vizitării:
10
5
7
3

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 3
        ┌── 5
    ┌── [ ]
        └── 2
        ┌── 8

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
3
Noduri frunză vizitate:
3
Ordinea vizitării:
3
5
2

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 4
        ┌── 4
    ┌── [ ]
        └── 4
        ┌── 4

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
4
Noduri frunză vizitate:
3
Ordinea vizitării:
4
4
4

```

```
Pentru arborele MinMax generat mai jos, aplicati algoritmul cu optimizarea Alpha-Beta si determinati valoarea radacinii si numarul de noduri vizitate.

└── [ ]
    └── [ ]
        └── 1
        ┌── 2
    ┌── [ ]
        └── 3
        ┌── 4

Raspuns:

Rezultat MinMax cu Alpha-Beta:
Valoarea rădăcinii:
3
Noduri frunză vizitate:
4
Ordinea vizitării:
1
2
3
4

```

## 4. STRATEGY

```
Pentru problema N-Queens cu N=4, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Backtracking (sau CSP standard)

```

```
Pentru problema N-Queens cu N=10, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Backtracking (sau CSP standard)

```


```
Pentru problema N-Queens cu N=15, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Backtracking (sau CSP standard)

```

```
Pentru problema N-Queens cu N=100, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema N-Queens cu N=1000, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema N-Queens cu N=100000, care este cea mai potrivita strategie de rezolvare dintre cele mentionate la curs pentru a gasi o solutie valida intr-un timp scurt?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema Turnurile din Hanoi cu 3 discuri, unde obiectivul este gasirea numarului MINIM de mutari, ce strategie de cautare este cea mai indicata?

Raspuns: BFS (Breadth First Search)

```

```
Pentru problema Turnurile din Hanoi cu 5 discuri, unde obiectivul este gasirea oricarei solutii valide (fara restrictie de optim), ce strategie de cautare este cea mai indicata?

Raspuns: DFS (sau Recursivitate / Divide et Impera)

```

```
Pentru problema Turnurile din Hanoi cu 3 discuri, unde obiectivul este gasirea oricarei solutii valide (fara restrictie de optim), ce strategie de cautare este cea mai indicata?

Raspuns: DFS (sau Recursivitate / Divide et Impera)

```

```
Pentru problema Turnurile din Hanoi cu 5 discuri, unde obiectivul este gasirea numarului MINIM de mutari, ce strategie de cautare este cea mai indicata?

Raspuns: BFS (Breadth First Search)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf cu 10 regiuni si multiple cicluri, care este cea mai eficienta strategie pentru a gasi o colorare valida sau a demonstra ca nu exista?

Raspuns: Backtracking (optimizat cu FC + MRV)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf cu 15 regiuni si multiple cicluri, care este cea mai eficienta strategie pentru a gasi o colorare valida sau a demonstra ca nu exista?

Raspuns: Backtracking (optimizat cu FC + MRV)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf cu 25 regiuni si multiple cicluri, care este cea mai eficienta strategie pentru a gasi o colorare valida sau a demonstra ca nu exista?

Raspuns: Backtracking (optimizat cu FC + MRV)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf arbore (fara cicluri) cu 15 noduri, care este cea mai eficienta strategie?

Raspuns: Tree-CSP (Arc Consistency + Sortare Topologică)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf arbore (fara cicluri) cu 30 noduri, care este cea mai eficienta strategie?

Raspuns: Tree-CSP (Arc Consistency + Sortare Topologică)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf arbore (fara cicluri) cu 50 noduri, care este cea mai eficienta strategie?

Raspuns: Tree-CSP (Arc Consistency + Sortare Topologică)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf masiv cu 5000 noduri si densitate ridicata, unde timpul de executie este critic, care este cea mai practica abordare?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf masiv cu 7500 noduri si densitate ridicata, unde timpul de executie este critic, care este cea mai practica abordare?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema Colorarea Hartilor (Graph Coloring) aplicata pe un graf masiv cu 10000 noduri si densitate ridicata, unde timpul de executie este critic, care este cea mai practica abordare?

Raspuns: Min-Conflicts (Căutare Locală)

```

```
Pentru problema Tura Calului (Knight's Tour) pe o tabla de 8x8, unde se doreste gasirea rapida a unei solutii, care este abordarea recomandata?

Raspuns: Regula lui Warnsdorff (Euristică Greedy)

```

```
Pentru problema Tura Calului (Knight's Tour) pe o tabla de 4x4, unde se doreste demonstrarea inexistentei unei solutii, care este abordarea recomandata?

Raspuns: Regula lui Warnsdorff (Euristică Greedy)

```
