from pydantic import BaseModel
from typing import List


class KnowledgeRequest(BaseModel):

    question: str


class KnowledgeResponse(BaseModel):

    question: str

    answer: str

    sources: List[str]