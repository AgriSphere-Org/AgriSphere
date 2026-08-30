import json
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()


class GeminiVisionService:
    """
    Uses Gemini Vision to analyze crop images.
    Returns structured crop health analysis.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def analyze_crop(
        self,
        image: Image.Image,
        farmer_crop: Optional[str] = None
    ) -> Dict:

        prompt = self._build_prompt(farmer_crop)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )

        return self._parse_response(response.text)

    def _build_prompt(self, farmer_crop: Optional[str]) -> str:

        return f"""
You are an expert agricultural vision AI.

Analyze the uploaded agricultural image carefully.

Farmer provided crop:
{farmer_crop if farmer_crop else "Not Provided"}

Tasks:

1. Identify the crop.
2. Compare detected crop with farmer crop.
3. Assess image quality.
4. Determine whether healthy or diseased.
5. If diseased, identify the most likely disease.
6. Estimate severity.
7. List visible symptoms.
8. Explain your reasoning briefly.
9. If image quality is poor, say so instead of guessing.

Return ONLY valid JSON.

Format:

{{
    "detected_crop": "",
    "crop_match": true,
    "image_quality": "",
    "health_status": "",
    "disease": "",
    "severity": "",
    "visible_symptoms": [
        ""
    ],
    "analysis_summary": ""
}}

Do not return markdown.
Do not use ```json.
Only JSON.
"""

    def _parse_response(self, response_text: str) -> Dict:

        response_text = response_text.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "").strip()

        return json.loads(response_text)