from fastapi import APIRouter

from models.exam import (
    ClozeRequest,
    ClozeResponse,
    EvaluateSentenceRequest,
    EvaluateSentenceResponse,
)
from services.exam_service import exam_service

router = APIRouter(prefix="/exam", tags=["exam"])


@router.post("/cloze", response_model=ClozeResponse)
def generate_cloze(request: ClozeRequest):
    """Sinh câu điền từ Cloze AI; server xáo thứ tự 4 đáp án."""
    return exam_service.generate_cloze(request)


@router.post("/evaluate-sentence", response_model=EvaluateSentenceResponse)
def evaluate_sentence(request: EvaluateSentenceRequest):
    """Chấm bài Sentence Writing AI (score 0–10)."""
    return exam_service.evaluate_sentence(request)
