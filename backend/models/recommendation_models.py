from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    climate_data: Dict[str, Any] = Field(default_factory=dict)
    crop_plan: Dict[str, Any] = Field(default_factory=dict)
    crop_health: Dict[str, Any] = Field(default_factory=dict)
    market_data: Dict[str, Any] = Field(default_factory=dict)
    government_schemes: List[Dict[str, Any]] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    recommended_crop: str
    recommended_season: str
    irrigation_advice: str
    fertilizer_advice: str
    disease_prevention: str
    harvest_recommendation: str
    selling_recommendation: str
    government_schemes: List[str] = Field(default_factory=list)
    overall_risk: str
    overall_summary: str
    ai_report: str