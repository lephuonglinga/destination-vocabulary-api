from fastapi import APIRouter

from models.coach import (
    EvaluateRequest,
    EvaluateResponse,
    ExplainRequest,
    ExplainResponse,
)
from services.coach_service import coach_service

router = APIRouter(prefix="/coach", tags=["coach"])


@router.post("/explain", response_model=ExplainResponse)
def explain_word(request: ExplainRequest):
    """Feedback từ vựng: khi nào dùng, hoàn cảnh, ví dụ."""
    return coach_service.explain(request)


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_sentence(request: EvaluateRequest):
    """Feedback câu học sinh viết: ngữ pháp, từ vựng, tự nhiên, gợi ý."""
    return coach_service.evaluate(request)
