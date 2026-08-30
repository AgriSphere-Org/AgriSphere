"""
Gemini service for the AgriSphere Recommendation Agent.

This service uses Gemini to independently generate agricultural
recommendations based on:
    - Crop
    - State
    - Soil pH

It does not depend on outputs from other AgriSphere agents.
"""

import json
import logging
import os
import re
from typing import Dict

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from models.recommendation_models import RecommendationResponse


load_dotenv()

logger = logging.getLogger("agrisphere.gemini_recommendation")


class GeminiRecommendationService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = "gemini-2.5-flash"

    # ==========================================================
    # MAIN METHOD
    # ==========================================================

    def generate_recommendation(
        self,
        crop: str,
        state: str,
        soil_ph: float
    ) -> Dict:

        prompt = self._build_prompt(
            crop=crop,
            state=state,
            soil_ph=soil_ph
        )

        try:

            logger.info(
                "Sending recommendation request to Gemini."
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            if not response or not response.text:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            cleaned_response = self._clean_json_response(
                response.text
            )

            result = json.loads(
                cleaned_response
            )

            # Validate Gemini output
            validated = RecommendationResponse.model_validate(
                result
            )

            return validated.model_dump()

        except APIError as e:

            logger.error(
                "Gemini API error: %s",
                str(e)
            )

            raise RuntimeError(
                f"Gemini API error: {str(e)}"
            ) from e

        except json.JSONDecodeError as e:

            logger.error(
                "Invalid JSON returned by Gemini: %s",
                str(e)
            )

            raise ValueError(
                "Gemini returned an invalid JSON response."
            ) from e

        except Exception as e:

            logger.error(
                "Recommendation generation failed: %s",
                str(e),
                exc_info=True
            )

            raise

    # ==========================================================
    # GEMINI PROMPT
    # ==========================================================

    def _build_prompt(
        self,
        crop: str,
        state: str,
        soil_ph: float
    ) -> str:

        return f"""
You are the AgriSphere Agricultural Recommendation Agent.

You are an independent agricultural advisor.

Your job is to provide practical recommendations to a farmer
based on the information provided below.

IMPORTANT:

You are NOT a summarization agent.

You are NOT combining recommendations from other agents.

You are making your OWN agricultural assessment.

============================================================
FARMER INPUT
============================================================

Crop:
{crop}

State:
{state}

Soil pH:
{soil_ph}

============================================================
YOUR TASK
============================================================

Analyze the provided crop, state and soil pH.

Generate useful agricultural recommendations relevant to
growing this crop in the given state and soil condition.

Consider, where relevant:

1. Soil management
2. Nutrient management
3. Irrigation
4. Crop management
5. Pest and disease prevention
6. Weed management
7. Growth management
8. Harvest management
9. General risk prevention

Do NOT force every category into the answer.

Only include recommendations that are relevant.

============================================================
IMPORTANT REASONING RULES
============================================================

- Use your agricultural knowledge to reason about the inputs.
- Do not simply repeat the input.
- Prioritize the most useful actions.
- Give practical advice that a farmer can understand.
- Explain the reason behind each recommendation.
- Do not invent current weather conditions.
- Do not invent current market prices.
- Do not invent government schemes.
- Do not claim that a disease exists unless there is evidence.
- Do not give dangerous or highly specific chemical instructions.
- Do not invent exact fertilizer or pesticide doses.
- If important information is missing, mention it in limitations.
- Do not treat assumptions as confirmed facts.

The state should be used as regional context, but do not invent
specific local conditions that were not provided.

============================================================
RISK
============================================================

Assign an overall agricultural risk based only on the available
information.

Allowed values:

Low
Moderate
High
Critical

Do not assign High or Critical risk without sufficient reason.

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use ```json.

Do NOT add any text before or after the JSON.

Use exactly this structure:

{{
    "crop": "{crop}",
    "state": "{state}",
    "soil_ph": {soil_ph},

    "recommendations": [
        {{
            "priority": 1,
            "area": "Soil Management",
            "recommendation": "Practical recommendation",
            "reason": "Agricultural reason for this recommendation"
        }}
    ],

    "overall_risk": "Low",

    "overall_advice": "Short practical advice for the farmer.",

    "limitations": [
        "Important information that was not available."
    ]
}}

============================================================
FINAL REQUIREMENT
============================================================

The recommendations must be generated specifically for the
provided crop, state and soil pH.

Do not make the response a generic agricultural summary.

The Recommendation Agent must provide actual actionable
recommendations.
"""

    # ==========================================================
    # CLEAN GEMINI RESPONSE
    # ==========================================================

    def _clean_json_response(
        self,
        text: str
    ) -> str:

        text = text.strip()

        # Remove ```json
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        # Remove closing ```
        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        return text.strip()