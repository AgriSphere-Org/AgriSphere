import sys
import os

# Ensures backend directory is added to Python path for relative/package imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, HTTPException, status

from agents.recommendation_agent import RecommendationAgent
from models.recommendation_models import (
    RecommendationRequest,
    RecommendationResponse
)

router = APIRouter(
    prefix="/recommendation",
    tags=["Final Recommendation"]
)

agent = RecommendationAgent()


@router.post(
    "/generate",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Comprehensive Farming Recommendations",
    description="Combines insights from Climate, Crop Planning, Crop Health, Market Intelligence, and Government Scheme agents to generate unified actionable recommendations."
)
def generate_recommendation(
    request: RecommendationRequest
) -> RecommendationResponse:
    try:
        result = agent.generate_recommendation(
            climate_data=request.climate_data,
            crop_plan=request.crop_plan,
            crop_health=request.crop_health,
            market_data=request.market_data,
            government_schemes=request.government_schemes
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendation: {str(e)}"
        )