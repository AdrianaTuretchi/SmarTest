from typing import List, Optional, Tuple
from pydantic import BaseModel
from typing import Dict, Any


class NashQuestionResponse(BaseModel):
    question_text: str
    raw_data: List[List[List[int]]]
    template_id: Optional[str]


class NashSubmission(BaseModel):
    user_answer: str
    # raw_data is a matrix where each cell is [p1, p2]
    raw_data: List[List[List[int]]]


class EvaluationResponse(BaseModel):
    score: float
    correct_coords: List[Tuple[int, int]]
    feedback_text: Optional[str] = None


class CSPQuestionResponse(BaseModel):
    question_text: str
    raw_data: Dict[str, Any]
    template_id: Optional[str]


class CSPSubmission(BaseModel):
    user_answer: Dict[str, int]
    raw_data: Dict[str, Any]
    template_id: Optional[str] = None


class CSPEvaluationResponse(BaseModel):
    score: float
    correct_assignment: Dict[str, int]
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