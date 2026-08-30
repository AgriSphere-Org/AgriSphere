"""
Gemini service for the AgriSphere Recommendation Agent.

The Recommendation Agent is standalone.

Input:
    - crop
    - state
    - soil_ph

Output:
    - crop
    - state
    - soil_ph
    - recommendations
    - overall_advice
"""

import json
import logging
import os
import re
from typing import Dict

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError


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
            crop,
            state,
            soil_ph
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

            result = json.loads(cleaned_response)

            return result

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
                "Gemini returned invalid JSON: %s",
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
You are the AgriSphere Recommendation Agent.

You are an independent agricultural recommendation system.

You receive only three inputs:

Crop: {crop}
State: {state}
Soil pH: {soil_ph}

Your task is to generate practical agricultural recommendations
for the farmer.

You must use the provided crop, state and soil pH as the main
context for your recommendations.

Do NOT depend on outputs from any other AgriSphere agent.

Do NOT ask the farmer for additional information.

Do NOT summarize other agents.

Do NOT create a general essay about the crop.

Instead, provide a small number of useful and actionable
recommendations.

Consider areas such as:

- Soil
- Nutrients
- Water
- Crop Protection
- Crop Management
- Weed Management
- Harvest Management

Only include areas that are relevant.

Give approximately 4 recommendations.

Prioritize the most useful recommendations first.

Keep every recommendation short, clear and practical so that
a farmer can easily understand it.

Do not provide a separate reason field.

Do not provide risk analysis.

Do not provide limitations.

Do not provide market prices.

Do not provide government schemes.

Do not invent current weather conditions.

Do not invent farm-specific facts that were not provided.

Use general agricultural knowledge when necessary, but clearly
base the recommendations on the available inputs.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use ```json.

Do NOT add any text before or after the JSON.

Return exactly this structure:

{{
    "crop": "{crop}",
    "state": "{state}",
    "soil_ph": {soil_ph},
    "recommendations": [
        {{
            "priority": 1,
            "area": "Soil",
            "recommendation": "Short practical recommendation."
        }},
        {{
            "priority": 2,
            "area": "Nutrients",
            "recommendation": "Short practical recommendation."
        }},
        {{
            "priority": 3,
            "area": "Water",
            "recommendation": "Short practical recommendation."
        }},
        {{
            "priority": 4,
            "area": "Crop Protection",
            "recommendation": "Short practical recommendation."
        }}
    ],
    "overall_advice": "Short overall advice for the farmer."
}}

IMPORTANT:

- Keep recommendations concise.
- Do not add extra JSON fields.
- Do not add "reason".
- Do not add "risk".
- Do not add "limitations".
- Do not add "agent_outputs".
- Do not ask questions.
"""
        return prompt

    # ==========================================================
    # CLEAN JSON RESPONSE
    # ==========================================================

    def _clean_json_response(
        self,
        text: str
    ) -> str:

        text = text.strip()

        # Remove Markdown JSON fences if Gemini adds them
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        return text.strip()