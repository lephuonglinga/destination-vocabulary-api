from typing import Literal

from pydantic import BaseModel, Field


class ClozeRequest(BaseModel):
    word: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)
    level: Literal["b1", "b2", "c1&c2"]


class ClozeResponse(BaseModel):
    sentence: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str


class EvaluateSentenceRequest(BaseModel):
    word: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)
    sentence: str = Field(..., min_length=1)


class EvaluateSentenceResponse(BaseModel):
    score: int = Field(..., ge=0, le=10)
    grammar: str
    vocabulary: str
    naturalness: str
    suggestion: list[str] = Field(..., min_length=1, max_length=2)
