from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):

    climate_data: dict

    crop_plan: dict

    crop_health: dict

    market_data: dict

    government_schemes: List[dict]


class RecommendationResponse(BaseModel):

    recommended_crop: str

    recommended_season: str

    irrigation_advice: str

    fertilizer_advice: str

    disease_prevention: str

    harvest_recommendation: str

    selling_recommendation: str

    government_schemes: List[str]

    overall_risk: str

    overall_summary: str

    ai_report: str