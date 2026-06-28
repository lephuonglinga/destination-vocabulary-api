from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    word: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)


class ExampleItem(BaseModel):
    sentence: str
    note: str


class ExplainResponse(BaseModel):
    usage: str
    contexts: list[str] = Field(..., min_length=1, max_length=2)
    examples: list[ExampleItem] = Field(..., min_length=1, max_length=2)


class EvaluateRequest(BaseModel):
    word: str = Field(..., min_length=1)
    sentence: str = Field(..., min_length=1)


class EvaluateResponse(BaseModel):
    grammar: str
    vocabulary: str
    naturalness: str
    suggestion: list[str] = Field(..., min_length=1, max_length=2)
