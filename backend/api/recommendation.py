"""
FastAPI API for the AgriSphere Recommendation Agent.

The Recommendation Agent is an independent agent.

It accepts only:
    - crop
    - state
    - soil_ph

It does not require any other AgriSphere agent.
"""

import logging

from fastapi import APIRouter, HTTPException, status

from agents.recommendation_agent import RecommendationAgent
from models.recommendation_models import (
    RecommendationRequest,
    RecommendationResponse
)


logger = logging.getLogger("agrisphere.api.recommendation")


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendation Agent"]
)


# ==========================================================
# AGENT INSTANCE
# ==========================================================

recommendation_agent = RecommendationAgent()


# ==========================================================
# RECOMMENDATION ENDPOINT
# ==========================================================

@router.post(
    "/analyze",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate agricultural recommendations",
    description=(
        "Generates independent agricultural recommendations "
        "using crop, state and soil pH."
    )
)
async def generate_recommendation(
    request: RecommendationRequest
):

    try:

        logger.info(
            "Recommendation request received: "
            "crop=%s, state=%s, soil_pH=%s",
            request.crop,
            request.state,
            request.soil_ph
        )

        result = recommendation_agent.evaluate(
            request
        )

        return result

    except ValueError as e:

        logger.warning(
            "Invalid recommendation input: %s",
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    except RuntimeError as e:

        logger.error(
            "Recommendation service error: %s",
            str(e),
            exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )

    except Exception as e:

        logger.error(
            "Unexpected recommendation error: %s",
            str(e),
            exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Unable to generate agricultural recommendations."
            )
        )