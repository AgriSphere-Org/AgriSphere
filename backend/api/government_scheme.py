from fastapi import APIRouter, HTTPException

from agents.government_scheme_agent import GovernmentSchemeAgent

from models.government_scheme import (
    GovernmentSchemeRequest,
    GovernmentSchemeResponse
)

router = APIRouter(
    prefix="/government",
    tags=["Government Schemes"]
)

agent = GovernmentSchemeAgent()


@router.post(
    "/recommend",
    response_model=GovernmentSchemeResponse
)
def recommend_scheme(request: GovernmentSchemeRequest):

    try:

        recommendations = agent.recommend_schemes(

            state=request.state,

            farmer_category=request.farmer_category,

            purpose=request.purpose

        )

        return {
            "recommendations": recommendations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )