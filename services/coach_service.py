import json

import google.generativeai as genai
from fastapi import HTTPException

from config import settings
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


def _get_model():
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY chưa được cấu hình. Lấy key miễn phí tại https://aistudio.google.com/apikey",
        )

    genai.configure(api_key=settings.gemini_api_key)
    return genai.GenerativeModel(
        settings.gemini_model,
        system_instruction=None,
        generation_config={
            "temperature": 0.4,
            "response_mime_type": "application/json",
        },
    )


def _call_gemini(system: str, user: str) -> dict:
    model = _get_model()
    prompt = f"{system}\n\n{user}"

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail="LLM trả về JSON không hợp lệ",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        message = str(exc)
        if "429" in message or "quota" in message.lower():
            raise HTTPException(
                status_code=429,
                detail=(
                    "Hết quota Gemini free tier. Đổi GEMINI_MODEL sang "
                    "gemini-2.5-flash-lite hoặc gemini-2.5-flash trong .env, "
                    "đợi ~1 phút rồi thử lại. Chi tiết: https://ai.google.dev/gemini-api/docs/rate-limits"
                ),
            ) from exc
        raise HTTPException(
            status_code=502,
            detail=f"Lỗi khi gọi Gemini: {exc}",
        ) from exc


def _clamp_list(items: list, min_len: int, max_len: int) -> list:
    if len(items) > max_len:
        return items[:max_len]
    if len(items) < min_len and items:
        return items
    return items


class CoachService:
    def explain(self, request: ExplainRequest) -> ExplainResponse:
        payload = _call_gemini(
            EXPLAIN_SYSTEM,
            EXPLAIN_USER.format(
                word=request.word,
                definition=request.definition,
            ),
        )

        contexts = _clamp_list(payload.get("contexts", []), 1, 2)
        examples = _clamp_list(payload.get("examples", []), 1, 2)

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
        payload = _call_gemini(
            EVALUATE_SYSTEM,
            EVALUATE_USER.format(
                word=request.word,
                sentence=request.sentence,
            ),
        )

        suggestions = _clamp_list(payload.get("suggestion", []), 1, 2)
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
