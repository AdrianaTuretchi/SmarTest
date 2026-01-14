from typing import List, Optional, Tuple
from pydantic import BaseModel
from typing import Dict, Any


class NashQuestionResponse(BaseModel):
    question_text: str
    raw_data: List[List[List[int]]]
    template_id: Optional[str]
    requires_dominated: bool = False  # True dacă întrebarea cere și strategii dominate


class NashSubmission(BaseModel):
    user_answer: Optional[Any] = None  # String pentru Nash simplu, dict pentru extended, sau None
    # raw_data is a matrix where each cell is [p1, p2]
    raw_data: List[List[List[int]]]
    # Pentru întrebări cu strategii dominate
    requires_dominated: Optional[bool] = None  # Dacă întrebarea cere strategii dominate
    has_dominated: Optional[bool] = None  # Răspunsul utilizatorului: există strategii dominate?
    dominated_p1: Optional[List[int]] = None  # Strategiile dominate pentru jucătorul 1
    dominated_p2: Optional[List[int]] = None  # Strategiile dominate pentru jucătorul 2
    has_equilibrium: Optional[bool] = None  # Răspunsul utilizatorului: există echilibru Nash?


class EvaluationResponse(BaseModel):
    score: float
    correct_coords: List[Tuple[int, int]]
    feedback_text: Optional[str] = None
    # Pentru întrebări cu strategii dominate
    correct_dominated_p1: Optional[List[int]] = None
    correct_dominated_p2: Optional[List[int]] = None


class CSPQuestionResponse(BaseModel):
    question_text: str
    raw_data: Dict[str, Any]
    template_id: Optional[str]


class CSPSubmission(BaseModel):
    user_answer: Dict[str, int] 
    raw_data: Dict[str, Any]
    template_id: Optional[str] = None
    has_solution: Optional[bool] = None  # True/False/None - dacă utilizatorul crede că problema are soluție


class CSPEvaluationResponse(BaseModel):
    score: float
    correct_assignment: Optional[Dict[str, int]] = None
    has_solution: Optional[bool] = None  # True dacă problema are soluție, False altfel
    feedback_text: Optional[str] = None


class MinMaxQuestionResponse(BaseModel):
    question_text: str
    raw_data: Dict[str, Any]
    template_id: Optional[str]


class MinMaxSubmission(BaseModel):
    root_value: Optional[int] = None
    visited_count: Optional[int] = None
    raw_data: Dict[str, Any]


class MinMaxEvaluationResponse(BaseModel):
    score: float
    correct_root_value: int
    correct_visited_count: int
    feedback_text: Optional[str] = None


class StrategySubmission(BaseModel):
    user_answer: str
    raw_data: Dict[str, Any]
    template_id: Optional[str] = None

class StrategyQuestionResponse(BaseModel):
    question_text: str
    raw_data: Dict[str, Any]
    template_id: str

class StrategyEvaluationResponse(BaseModel):
    score: float
    correct_answer: Optional[str] = None
    feedback_text: Optional[str] = None


# Solver schemas
class SolveRequest(BaseModel):
    question_text: str


class SolveResponse(BaseModel):
    detected_type: str
    confidence: float
    extracted_data: Dict[str, Any]
    solution: Optional[Dict[str, Any]] = None
    justification: Optional[str] = None
    error_message: Optional[str] = None