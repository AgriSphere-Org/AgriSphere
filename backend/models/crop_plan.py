from pydantic import BaseModel
from typing import List


class CropPlanningRequest(BaseModel):

    city: str

    soil_ph: float


class CropRecommendation(BaseModel):

    crop: str

    season: str

    expected_profit: str

    climate_score: int

    soil_score: int

    confidence: int


class CropPlanningResponse(BaseModel):

    recommendations: List[CropRecommendation]