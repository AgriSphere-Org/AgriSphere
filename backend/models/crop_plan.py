from pydantic import BaseModel
from typing import List


class CropPlanningRequest(BaseModel):
    city: str
    soil_ph: float
    state: str | None = None


class CropRecommendation(BaseModel):
    crop: str
    category: str
    season: str

    expected_profit: str
    water_requirement: str
    duration_days: int

    climate_score: int
    soil_score: float
    region_score: int

    confidence: float

    suitability: str

    reasons: List[str]


class CropPlanningResponse(BaseModel):
    recommendations: List[CropRecommendation]