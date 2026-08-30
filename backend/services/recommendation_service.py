"""
Service layer for the AgriSphere Recommendation Agent.

This service connects the Recommendation Agent with the
Gemini Recommendation Service.

The agent is completely standalone and requires only:
    - crop
    - state
    - soil_ph
"""

import logging
from typing import Dict

from services.gemini_recommendation_service import (
    GeminiRecommendationService
)


logger = logging.getLogger("agrisphere.recommendation_service")


class RecommendationService:

    def __init__(self):

        self.gemini_service = GeminiRecommendationService()

    # ==========================================================
    # GENERATE RECOMMENDATION
    # ==========================================================

    def generate_recommendation(
        self,
        crop: str,
        state: str,
        soil_ph: float
    ) -> Dict:
        """
        Generate agricultural recommendations using Gemini.

        Inputs:
            crop
            state
            soil_ph
        """

        logger.info(
            "Generating recommendation for crop=%s, state=%s, soil_pH=%s",
            crop,
            state,
            soil_ph
        )

        # Basic validation
        if not crop or not crop.strip():
            raise ValueError(
                "Crop is required."
            )

        if not state or not state.strip():
            raise ValueError(
                "State is required."
            )

        if soil_ph < 0 or soil_ph > 14:
            raise ValueError(
                "Soil pH must be between 0 and 14."
            )

        # Send the three inputs to Gemini
        result = self.gemini_service.generate_recommendation(
            crop=crop,
            state=state,
            soil_ph=soil_ph
        )

        logger.info(
            "Recommendation generated successfully."
        )

        return result