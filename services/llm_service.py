import json

import google.generativeai as genai
from fastapi import HTTPException

from config import settings


def get_model():
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


def call_gemini(system: str, user: str) -> dict:
    model = get_model()
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


def clamp_list(items: list, min_len: int, max_len: int) -> list:
    if len(items) > max_len:
        return items[:max_len]
    return items
