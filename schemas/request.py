from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class PredictionRequest(BaseModel):
    query: str
    id: int


class PredictionResponse(BaseModel):
    id: int
    answer: Optional[int]
    reasoning: str
    sources: List[HttpUrl]
