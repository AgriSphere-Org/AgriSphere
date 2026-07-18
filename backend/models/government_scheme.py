from pydantic import BaseModel
from typing import List


class GovernmentSchemeRequest(BaseModel):

    state: str

    farmer_category: str

    farm_size: float

    crop: str

    irrigation: str

    gender: str

    age: int


class SchemeRecommendation(BaseModel):

    scheme_name: str

    benefit: str

    official_link: str

    confidence: int


class GovernmentSchemeResponse(BaseModel):

    recommendations: List[SchemeRecommendation]