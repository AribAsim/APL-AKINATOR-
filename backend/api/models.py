from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class SessionState(BaseModel):
    session_id: str
    probabilities: Dict[str, float]
    asked_questions: List[str] = Field(default_factory=list)
    question_count: int = 0
    stage: str = "HARD_FILTER" # HARD_FILTER or PROBABILISTIC
    last_attribute: Optional[str] = None
    answer_history: List[Dict[str, str]] = Field(default_factory=list) # List of {"attribute": attr, "answer": ans}
    disambiguation_mode: bool = False
    top_two_candidates: List[str] = Field(default_factory=list)
    max_questions: int = 8

class StartRequest(BaseModel):
    max_questions: Optional[int] = 8

class StartResponse(BaseModel):
    session_id: str
    question: str
    attribute: str
    confidence: float
    remaining_candidates: int
    banter: Optional[str] = None
    max_questions: int = 8

class AnswerRequest(BaseModel):
    session_id: str
    answer: str # yes, no, dont_know, probably, probably_not

class NextQuestionResponse(BaseModel):
    question: str
    attribute: str
    confidence: float
    remaining_candidates: int
    is_disambiguation: bool = False
    banter: Optional[str] = None

class GuessResponse(BaseModel):
    guess: str
    confidence: float
    banter: Optional[str] = None

class FeedbackRequest(BaseModel):
    session_id: str
    correct_player: str
    was_correct: bool

class StateResponse(BaseModel):
    top_candidates: List[Dict[str, Any]]
    question_count: int
    asked_questions: List[str]
    disambiguation_mode: bool
