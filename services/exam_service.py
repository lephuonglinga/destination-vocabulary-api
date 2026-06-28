import random

from fastapi import HTTPException

from models.exam import (
    ClozeRequest,
    ClozeResponse,
    EvaluateSentenceRequest,
    EvaluateSentenceResponse,
)
from prompts.exam import (
    CLOZE_SYSTEM,
    CLOZE_USER,
    EVALUATE_SENTENCE_SYSTEM,
    EVALUATE_SENTENCE_USER,
)
from services.llm_service import call_gemini, clamp_list
from services.vocabulary_service import pick_random_distractors, strip_term_label


def _shuffle_options(word: str, wrong_options: list[str]) -> list[str]:
    options = [word, *wrong_options[:3]]
    if len(set(options)) < 4:
        raise HTTPException(
            status_code=502,
            detail="Không đủ 4 đáp án khác nhau cho câu cloze",
        )
    random.shuffle(options)
    return options


class ExamService:
    def generate_cloze(self, request: ClozeRequest) -> ClozeResponse:
        word = strip_term_label(request.word)
        distractors = pick_random_distractors(request.level, word, 3)
        if len(distractors) < 3:
            raise HTTPException(
                status_code=400,
                detail="Level không đủ từ để tạo distractor",
            )

        payload = call_gemini(
            CLOZE_SYSTEM,
            CLOZE_USER.format(
                word=word,
                definition=request.definition,
            ),
        )

        sentence = payload.get("sentence", "")
        if "_____" not in sentence:
            raise HTTPException(
                status_code=502,
                detail="LLM trả về câu thiếu chỗ trống _____",
            )

        options = _shuffle_options(word, distractors)

        return ClozeResponse(
            sentence=sentence,
            options=options,
            correct_answer=word,
        )

    def evaluate_sentence(self, request: EvaluateSentenceRequest) -> EvaluateSentenceResponse:
        payload = call_gemini(
            EVALUATE_SENTENCE_SYSTEM,
            EVALUATE_SENTENCE_USER.format(
                word=request.word,
                definition=request.definition,
                sentence=request.sentence,
            ),
        )

        suggestions = clamp_list(payload.get("suggestion", []), 1, 2)
        if not suggestions:
            raise HTTPException(
                status_code=502,
                detail="LLM trả về thiếu suggestion",
            )

        try:
            score = int(payload.get("score", 0))
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=502,
                detail="LLM trả về score không hợp lệ",
            ) from exc

        return EvaluateSentenceResponse(
            score=max(0, min(10, score)),
            grammar=payload.get("grammar", ""),
            vocabulary=payload.get("vocabulary", ""),
            naturalness=payload.get("naturalness", ""),
            suggestion=suggestions,
        )


exam_service = ExamService()
