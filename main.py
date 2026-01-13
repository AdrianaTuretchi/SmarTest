from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from engine.question_service import QuestionService
from engine.evaluation_service import EvaluationService
from engine.question_parser import QuestionParser
from core_logic.nash_logic import find_pure_nash, find_dominated_strategies
from core_logic.csp_logic import backtrack as csp_backtrack, ac3
from core_logic.minmax_logic import dict_to_tree, minmax as minmax_compute
from core_logic.strategy_solver import StrategySolver
from schemas import (
    NashQuestionResponse,
    NashSubmission,
    EvaluationResponse,
    CSPQuestionResponse,
    CSPSubmission,
    CSPEvaluationResponse,
    MinMaxQuestionResponse,
    MinMaxSubmission,
    MinMaxEvaluationResponse,
    StrategySubmission,
    StrategyQuestionResponse,  # Add this import for Strategy questions
    StrategyEvaluationResponse,
    SolveRequest,
    SolveResponse,
)

# FastAPI app
app = FastAPI(title="SmarTest API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root and engine initialization
PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATES_PATH = PROJECT_ROOT.joinpath("assets", "json_output", "templates.json")

generator = QuestionService(str(TEMPLATES_PATH))
evaluator_service = EvaluationService()
question_parser = QuestionParser()


def _tuples_to_lists(matrix):
    """Convert any tuples in matrix cells to lists for JSON serialization."""
    return [[list(cell) for cell in row] for row in matrix]


@app.get("/generate/nash", response_model=NashQuestionResponse)
def generate_nash():
    """Generate a Nash question (matrix + text)."""
    result = generator.generate_question_by_type("nash")
    if not result or "error" in result:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to generate question"))

    raw_data = result.get("raw_data")
    if raw_data is None:
        raise HTTPException(status_code=500, detail="Generator did not return raw_data")

    raw_data_json = _tuples_to_lists(raw_data)

    return NashQuestionResponse(
        question_text=result.get("question_text", ""),
        raw_data=raw_data_json,
        template_id=result.get("template_id"),
        requires_dominated=result.get("requires_dominated", False),
    )


@app.post("/evaluate/nash", response_model=EvaluationResponse)
def evaluate_nash(payload: NashSubmission):
    """Evaluate a submitted answer against the provided raw_data matrix."""
    raw_data = payload.raw_data
    
    # Extract user_answer - poate fi string, dict, sau None
    user_answer = payload.user_answer
    
    # Dacă user_answer este un dict (extended Nash din frontend), extragem câmpurile
    has_dominated = payload.has_dominated
    dominated_p1 = payload.dominated_p1
    dominated_p2 = payload.dominated_p2
    has_equilibrium = payload.has_equilibrium
    equilibria_text = ""
    
    if isinstance(user_answer, dict):
        # Extended Nash - extragem din user_answer
        has_dominated = user_answer.get('has_dominated', has_dominated)
        dominated_p1 = user_answer.get('dominated_p1', dominated_p1) or []
        dominated_p2 = user_answer.get('dominated_p2', dominated_p2) or []
        has_equilibrium = user_answer.get('has_equilibrium', has_equilibrium)
        equilibria_text = user_answer.get('equilibria', '')
        user_answer = equilibria_text  # Pentru evaluarea echilibrelor
    elif user_answer is None:
        user_answer = ""

    try:
        correct_coords = find_pure_nash(raw_data)
        dominated = find_dominated_strategies(raw_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid raw_data: {e}")

    # Check if this is an extended submission (with dominated strategies)
    is_extended = has_dominated is not None or payload.requires_dominated
    
    if is_extended:
        # Use extended evaluation
        from engine.evaluators.nash_evaluator import NashEvaluator
        nash_eval = NashEvaluator()
        score, details = nash_eval.evaluate_extended(
            raw_data=raw_data,
            user_answer=user_answer,
            has_dominated=has_dominated,
            dominated_p1=dominated_p1,
            dominated_p2=dominated_p2,
            has_equilibrium=has_equilibrium
        )
        
        # Build feedback text
        feedback_parts = []
        if 'dominated_existence' in details['scores']:
            if details['scores']['dominated_existence'] == 1.0:
                feedback_parts.append("\u2713 Ai r\u0103spuns corect despre existen\u021ba strategiilor dominate.")
            else:
                feedback_parts.append("\u2717 R\u0103spunsul despre existen\u021ba strategiilor dominate este incorect.")
        
        if 'dominated_identification' in details['scores']:
            if details['scores']['dominated_identification'] >= 0.8:
                feedback_parts.append("\u2713 Ai identificat corect strategiile dominate.")
            elif details['scores']['dominated_identification'] > 0:
                feedback_parts.append("~ Ai identificat par\u021bial strategiile dominate.")
            else:
                feedback_parts.append("\u2717 Nu ai identificat corect strategiile dominate.")
        
        if 'equilibrium_existence' in details['scores']:
            if details['scores']['equilibrium_existence'] == 1.0:
                feedback_parts.append("\u2713 Ai r\u0103spuns corect despre existen\u021ba echilibrului Nash.")
            else:
                feedback_parts.append("\u2717 R\u0103spunsul despre existen\u021ba echilibrului Nash este incorect.")
        
        if 'equilibrium_coords' in details['scores']:
            if details['scores']['equilibrium_coords'] >= 0.8:
                feedback_parts.append("\u2713 Ai identificat corect echilibrele Nash.")
            elif details['scores']['equilibrium_coords'] > 0:
                feedback_parts.append("~ Ai identificat par\u021bial echilibrele Nash.")
            else:
                feedback_parts.append("\u2717 Nu ai identificat corect echilibrele Nash.")
        
        feedback_text = "\n".join(feedback_parts)
        
        return EvaluationResponse(
            score=score, 
            correct_coords=correct_coords, 
            feedback_text=feedback_text,
            correct_dominated_p1=dominated['player1'],
            correct_dominated_p2=dominated['player2']
        )
    else:
        # Standard evaluation (just equilibrium)
        try:
            score, feedback_text = evaluator_service.evaluate('nash', payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return EvaluationResponse(score=score, correct_coords=correct_coords, feedback_text=feedback_text)


@app.get("/generate/csp", response_model=CSPQuestionResponse)
def generate_csp():
    """Generate a CSP question (variables/domains/constraints + text)."""
    result = generator.generate_question_by_type("csp")
    if not result or "error" in result:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to generate CSP question"))

    raw_data = result.get("raw_data")
    if raw_data is None:
        raise HTTPException(status_code=500, detail="Generator did not return raw_data for CSP")

    return CSPQuestionResponse(
        question_text=result.get("question_text", ""),
        raw_data=raw_data,
        template_id=result.get("template_id"),
    )


@app.post("/evaluate/csp", response_model=CSPEvaluationResponse)
def evaluate_csp(payload: CSPSubmission):
    """Evaluate a CSP submission: user_answer is a dict mapping variable->value."""
    user_answer = payload.user_answer
    raw_data = payload.raw_data

    # Recompute correct solution using csp_backtrack (from core_logic.csp_logic)
    try:
        variables = raw_data['variables']
        domains = raw_data['domains']
        constraints = raw_data['constraints']
        partial_assignment = raw_data.get('partial_assignment', {})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid raw_data structure: {e}")

    correct = csp_backtrack(variables, domains, constraints, partial_assignment)

    # evaluate via EvaluationService
    try:
        score, feedback_text = evaluator_service.evaluate('csp', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return CSPEvaluationResponse(score=score, correct_assignment=correct or {}, feedback_text=feedback_text)


@app.get("/generate/minmax", response_model=MinMaxQuestionResponse)
def generate_minmax():
    """Generate a MinMax question (binary tree + text)."""
    result = generator.generate_question_by_type("minmax")
    if not result or "error" in result:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to generate MinMax question"))

    raw_data = result.get("raw_data")
    if raw_data is None:
        raise HTTPException(status_code=500, detail="Generator did not return raw_data for MinMax")

    return MinMaxQuestionResponse(
        question_text=result.get("question_text", ""),
        raw_data=raw_data,
        template_id=result.get("template_id"),
    )


@app.post("/evaluate/minmax", response_model=MinMaxEvaluationResponse)
def evaluate_minmax(payload: MinMaxSubmission):
    """Evaluate a MinMax submission."""
    # Recompute correct answers
    try:
        tree = dict_to_tree(payload.raw_data)
        visited = []
        correct_root = minmax_compute(tree, 0, float('-inf'), float('inf'), True, visited)
        correct_visited = len(visited)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid raw_data: {e}")

    try:
        score, feedback_text = evaluator_service.evaluate('minmax', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return MinMaxEvaluationResponse(score=score, correct_root_value=correct_root, correct_visited_count=correct_visited, feedback_text=feedback_text)

@app.get("/generate/strategy", response_model=StrategyQuestionResponse)
def get_strategy_question():
    """
    Generates a new Strategy Selection question.
    This uses the StrategyGenerator to create dynamic instances (e.g., N=100 vs N=5).
    """
    result = generator.generate_question_by_type("strategy")
    if not result or "error" in result:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to generate Strategy question"))

    return StrategyQuestionResponse(
        question_text=result.get("question_text", ""),
        raw_data=result.get("raw_data"),
        template_id=result.get("template_id"),
    )

@app.post("/evaluate/strategy", response_model=StrategyEvaluationResponse)
def evaluate_strategy(payload: StrategySubmission):
    """
    Evaluates a strategy selection answer (e.g., choosing an algorithm).
    """
    try:
        score, feedback_text, correct_answer = evaluator_service.evaluate('strategy', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return StrategyEvaluationResponse(score=score, feedback_text=feedback_text, correct_answer=correct_answer)


@app.post("/solve", response_model=SolveResponse)
def solve_question(request: SolveRequest):
    """
    Parsează o întrebare din text, detectează tipul și returnează soluția.
    Suportă: Nash, CSP, Strategy. MinMax - suport parțial.
    """
    # Parsăm întrebarea
    parsed = question_parser.parse(request.question_text)
    
    if parsed.question_type == 'unknown' or parsed.error_message:
        return SolveResponse(
            detected_type=parsed.question_type,
            confidence=parsed.confidence,
            extracted_data=parsed.extracted_data,
            error_message=parsed.error_message
        )
    
    # Rezolvăm în funcție de tip
    solution = None
    justification = None
    error_message = None
    
    try:
        if parsed.question_type == 'nash':
            # Rezolvăm Nash
            if 'raw_data' in parsed.extracted_data:
                matrix = parsed.extracted_data['raw_data']
                equilibria = find_pure_nash(matrix)
                dominated = find_dominated_strategies(matrix)
                asks_dominated = parsed.extracted_data.get('asks_dominated', False)
                
                solution = {
                    'equilibria': equilibria,
                    'count': len(equilibria)
                }
                
                # Adăugăm strategiile dominate DOAR dacă întrebarea le cere explicit
                if asks_dominated:
                    solution['dominated'] = dominated
                    solution['has_dominated'] = bool(dominated['player1'] or dominated['player2'])
                
                # Construim justificarea
                justification_parts = []
                
                # Partea despre strategii dominate (dacă se cere)
                if asks_dominated:
                    if dominated['player1'] or dominated['player2']:
                        dom_parts = []
                        if dominated['player1']:
                            dom_parts.append(f"Jucătorul 1: strategiile {', '.join([f'S{i+1} (rând {i})' for i in dominated['player1']])}")
                        if dominated['player2']:
                            dom_parts.append(f"Jucătorul 2: strategiile {', '.join([f'S{i+1} (col {i})' for i in dominated['player2']])}")
                        justification_parts.append(f"DA, există strategii strict dominate. {'; '.join(dom_parts)}. O strategie este dominată dacă există o altă strategie care oferă un payoff mai mare indiferent de alegerea adversarului.")
                    else:
                        justification_parts.append("NU, nu există strategii strict dominate în această matrice. Nicio strategie nu este dominată de o alta pentru niciunul dintre jucători.")
                
                # Partea despre echilibre Nash
                if equilibria:
                    justification_parts.append(f"Echilibrele Nash pure găsite: {', '.join([f'({e[0]}, {e[1]})' for e in equilibria])}. Un echilibru Nash apare când niciun jucător nu poate îmbunătăți unilateral câștigul său.")
                else:
                    justification_parts.append("Nu există echilibre Nash pure în această matrice. Jocul poate avea doar echilibre în strategii mixte.")
                
                justification = "\n\n".join(justification_parts)
            else:
                error_message = "Nu am putut extrage matricea de payoff din text."
        
        elif parsed.question_type == 'csp':
            # Rezolvăm CSP
            data = parsed.extracted_data
            if 'variables' in data and 'domains' in data:
                variables = data['variables']
                domains = data['domains']
                constraints = data.get('constraints', [])
                partial_assignment = data.get('partial_assignment', {})
                
                # Formatăm constrângerile pentru solver - trebuie să fie tuple (v1, v2)
                constraint_list = []
                for c in constraints:
                    if len(c) == 2:
                        constraint_list.append((c[0], c[1]))  # Tuple simplu, != este implicit în solver
                
                # Încercăm backtracking cu asignarea parțială
                try:
                    result = csp_backtrack(variables, domains, constraint_list, partial_assignment.copy(), use_mrv=True, use_fc=True)
                    if result:
                        solution = {
                            'assignment': result,
                            'method': 'Backtracking cu MRV și Forward Checking'
                        }
                        # Formatăm cu culori pentru graph coloring
                        color_names = {1: 'Roșu', 2: 'Verde', 3: 'Albastru', 4: 'Galben'}
                        if 'graph-coloring' in data.get('tags', []):
                            assignment_str = ', '.join([f'{k}={color_names.get(v, v)}' for k, v in sorted(result.items())])
                        else:
                            assignment_str = ', '.join([f'{k}={v}' for k, v in sorted(result.items())])
                        justification = f"Soluție găsită: {assignment_str}. Am folosit Backtracking cu euristica MRV (Minimum Remaining Values) și Forward Checking pentru eficiență."
                    else:
                        solution = {'assignment': None, 'consistent': False}
                        justification = "Problema CSP nu are soluție - constrângerile sunt inconsistente."
                except Exception as e:
                    error_message = f"Eroare la rezolvarea CSP: {str(e)}"
            else:
                error_message = "Nu am putut extrage variabilele și domeniile din text."
        
        elif parsed.question_type == 'strategy':
            # Rezolvăm Strategy
            data = parsed.extracted_data
            solver = StrategySolver()
            
            strategy, justification_key = solver.solve(data)
            solution = {
                'recommended_strategy': strategy,
                'problem_type': data.get('problem_type', 'unknown')
            }
            
            # Generăm justificarea
            if data.get('problem_type') == 'n-queens':
                n = data.get('n', 'necunoscut')
                if isinstance(n, int) and n > 20:
                    justification = f"Pentru N-Queens cu N={n} (instanță mare), recomandăm {strategy}. Spațiul de căutare este prea mare pentru algoritmi sistematici, iar căutarea locală găsește soluții rapid."
                else:
                    justification = f"Pentru N-Queens cu N={n}, recomandăm {strategy}. Backtracking cu Forward Checking și MRV este eficient pentru instanțe de dimensiune medie."
            elif data.get('problem_type') == 'graph-coloring':
                if data.get('is_tree'):
                    justification = f"Pentru colorarea unui graf arbore, recomandăm {strategy}. Arborii au proprietatea că sunt 2-colorabili și pot fi rezolvați în timp liniar."
                else:
                    justification = f"Pentru colorarea grafului, recomandăm {strategy}."
            else:
                justification = f"Strategia recomandată: {strategy}"
        
        elif parsed.question_type == 'minmax':
            # Rezolvăm MinMax
            data = parsed.extracted_data
            if 'raw_data' in data and data['raw_data']:
                try:
                    from core_logic.minmax_logic import dict_to_tree, minmax
                    
                    # Reconstruim arborele
                    tree = dict_to_tree(data['raw_data'])
                    
                    # Aplicăm algoritmul MinMax cu Alpha-Beta
                    visited = []
                    root_value = minmax(tree, 0, float('-inf'), float('inf'), True, visited)
                    
                    solution = {
                        'root_value': root_value,
                        'visited_count': len(visited),
                        'visited_nodes': visited
                    }
                    
                    justification = (
                        f"Valoarea rădăcinii: {root_value}\n"
                        f"Noduri frunză vizitate: {len(visited)}\n"
                        f"Ordinea vizitării: {visited}\n\n"
                        f"Am aplicat algoritmul MinMax cu optimizarea Alpha-Beta. "
                        f"Rădăcina este un nod MAX. Alpha-Beta pruning a permis eliminarea "
                        f"ramurilor care nu pot influența rezultatul final."
                    )
                except Exception as e:
                    error_message = f"Eroare la rezolvarea MinMax: {str(e)}"
            else:
                error_message = "Nu am putut extrage arborele MinMax din text."
    
    except Exception as e:
        error_message = f"Eroare la rezolvare: {str(e)}"
    
    return SolveResponse(
        detected_type=parsed.question_type,
        confidence=parsed.confidence,
        extracted_data=parsed.extracted_data,
        solution=solution,
        justification=justification,
        error_message=error_message
    )