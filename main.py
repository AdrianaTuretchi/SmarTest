from pathlib import Path
from fastapi import FastAPI, HTTPException

from engine.question_service import QuestionService
from engine.evaluation_service import EvaluationService
from core_logic.nash_logic import find_pure_nash
from core_logic.csp_logic import backtrack as csp_backtrack
from core_logic.minmax_logic import dict_to_tree, minmax as minmax_compute
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
)

# FastAPI app
app = FastAPI(title="SmarTest API")

# Project root and engine initialization
PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATES_PATH = PROJECT_ROOT.joinpath("assets", "json_output", "templates.json")

generator = QuestionService(str(TEMPLATES_PATH))
evaluator_service = EvaluationService()


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
    )


@app.post("/evaluate/nash", response_model=EvaluationResponse)
def evaluate_nash(payload: NashSubmission):
    """Evaluate a submitted answer against the provided raw_data matrix."""
    user_answer = payload.user_answer
    raw_data = payload.raw_data

    try:
        correct_coords = find_pure_nash(raw_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid raw_data: {e}")

    try:
        score = evaluator_service.evaluate('nash', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return EvaluationResponse(score=score, correct_coords=correct_coords)


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
        score = evaluator_service.evaluate('csp', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return CSPEvaluationResponse(score=score, correct_assignment=correct or {})


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
        score = evaluator_service.evaluate('minmax', payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return MinMaxEvaluationResponse(score=score, correct_root_value=correct_root, correct_visited_count=correct_visited)
