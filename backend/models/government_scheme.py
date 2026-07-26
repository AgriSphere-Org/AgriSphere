from pydantic import BaseModel
from typing import List


class GovernmentSchemeRequest(BaseModel):
    state: str
    farmer_category: str
    purpose: str


class SchemeRecommendation(BaseModel):
    scheme_name: str

    description: str

    benefit: str

    eligibility: str

    application_status: str

    progress_percentage: int

    official_apply_url: str

    last_updated: str

    confidence: int


class GovernmentSchemeResponse(BaseModel):
    recommendations: List[SchemeRecommendation]