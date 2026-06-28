from fastapi import HTTPException

from models.coach import (
    EvaluateRequest,
    EvaluateResponse,
    ExplainRequest,
    ExplainResponse,
)
from prompts.coach import (
    EVALUATE_SYSTEM,
    EVALUATE_USER,
    EXPLAIN_SYSTEM,
    EXPLAIN_USER,
)
from services.llm_service import call_gemini, clamp_list


class CoachService:
    def explain(self, request: ExplainRequest) -> ExplainResponse:
        payload = call_gemini(
            EXPLAIN_SYSTEM,
            EXPLAIN_USER.format(
                word=request.word,
                definition=request.definition,
            ),
        )

        contexts = clamp_list(payload.get("contexts", []), 1, 2)
        examples = clamp_list(payload.get("examples", []), 1, 2)

        if not contexts or not examples:
            raise HTTPException(
                status_code=502,
                detail="LLM trả về thiếu contexts hoặc examples",
            )

        return ExplainResponse(
            usage=payload.get("usage", ""),
            contexts=contexts,
            examples=examples,
        )

    def evaluate(self, request: EvaluateRequest) -> EvaluateResponse:
        payload = call_gemini(
            EVALUATE_SYSTEM,
            EVALUATE_USER.format(
                word=request.word,
                sentence=request.sentence,
            ),
        )

        suggestions = clamp_list(payload.get("suggestion", []), 1, 2)
        if not suggestions:
            raise HTTPException(
                status_code=502,
                detail="LLM trả về thiếu suggestion",
            )

        return EvaluateResponse(
            grammar=payload.get("grammar", ""),
            vocabulary=payload.get("vocabulary", ""),
            naturalness=payload.get("naturalness", ""),
            suggestion=suggestions,
        )


coach_service = CoachService()
