from fastapi import APIRouter, HTTPException

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

    response_model=RecommendationResponse

)

def generate_recommendation(

    request: RecommendationRequest

):

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

            status_code=500,

            detail=str(e)

        )