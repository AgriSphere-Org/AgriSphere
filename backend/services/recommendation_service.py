"""
Service layer for the AgriSphere Recommendation Agent.

The Recommendation Agent is standalone and uses only:
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
        Generate independent agricultural recommendations.
        """

        # ------------------------------------------------------
        # Validate crop
        # ------------------------------------------------------

        if not crop or not crop.strip():
            raise ValueError("Crop is required.")

        # ------------------------------------------------------
        # Validate state
        # ------------------------------------------------------

        if not state or not state.strip():
            raise ValueError("State is required.")

        # ------------------------------------------------------
        # Validate soil pH
        # ------------------------------------------------------

        if soil_ph < 0 or soil_ph > 14:
            raise ValueError(
                "Soil pH must be between 0 and 14."
            )

        logger.info(
            "Generating recommendation for %s in %s with soil pH %.2f",
            crop,
            state,
            soil_ph
        )

        # ------------------------------------------------------
        # Ask Gemini for recommendations
        # ------------------------------------------------------

        result = self.gemini_service.generate_recommendation(
            crop=crop,
            state=state,
            soil_ph=soil_ph
        )

        # ------------------------------------------------------
        # Make sure basic fields match the farmer's input
        # ------------------------------------------------------

        result["crop"] = crop
        result["state"] = state
        result["soil_ph"] = soil_ph

        logger.info(
            "Recommendation generated successfully."
        )

        return result