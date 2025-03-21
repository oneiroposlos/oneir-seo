from typing import List

from pydantic import BaseModel


class ExtractMoodModel(BaseModel):
    mood: str
    confidence: int
    reasoning: str


class SuggestKeywordsModel(BaseModel):
    mood: List[str]
    theme: List[str]
    topic: List[str]
    activity: List[str]
