"""
AgriSphere Recommendation Agent.

This is a standalone agricultural recommendation agent.

Required inputs:
    - crop
    - state
    - soil_ph

The agent does not depend on any other AgriSphere agent.
"""

import logging
from typing import Dict

from models.recommendation_models import (
    RecommendationRequest,
    RecommendationResponse
)

from services.recommendation_service import (
    RecommendationService
)


logger = logging.getLogger("agrisphere.recommendation_agent")


class RecommendationAgent:

    def __init__(self):

        self.service = RecommendationService()

    # ==========================================================
    # MAIN AGENT METHOD
    # ==========================================================

    def evaluate(
        self,
        request: RecommendationRequest
    ) -> Dict:
        """
        Evaluate the farmer's information and generate
        independent agricultural recommendations.
        """

        logger.info(
            "Recommendation Agent started."
        )

        # ------------------------------------------------------
        # Validate input
        # ------------------------------------------------------

        if not request.crop.strip():
            raise ValueError(
                "Crop is required."
            )

        if not request.state.strip():
            raise ValueError(
                "State is required."
            )

        if request.soil_ph < 0 or request.soil_ph > 14:
            raise ValueError(
                "Soil pH must be between 0 and 14."
            )

        # ------------------------------------------------------
        # Generate recommendation
        # ------------------------------------------------------

        result = self.service.generate_recommendation(
            crop=request.crop,
            state=request.state,
            soil_ph=request.soil_ph
        )

        # ------------------------------------------------------
        # Validate final response
        # ------------------------------------------------------

        validated_response = RecommendationResponse.model_validate(
            result
        )

        logger.info(
            "Recommendation Agent completed successfully."
        )

        return validated_response.model_dump()