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

            farm_size=request.farm_size,

            crop=request.crop,

            irrigation=request.irrigation,

            gender=request.gender,

            age=request.age

        )

        return {

            "recommendations": recommendations

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )