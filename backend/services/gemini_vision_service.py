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

        # ---------------------------------------------------
        # Resize large images before sending them to Gemini
        # This reduces upload/processing time while keeping
        # enough resolution for crop-health analysis.
        # ---------------------------------------------------

        image = image.copy()

        image.thumbnail((1280, 1280))

        # ---------------------------------------------------
        # Build prompt
        # ---------------------------------------------------

        prompt = self._build_prompt(farmer_crop)

        # ---------------------------------------------------
        # Gemini Vision analysis
        # ---------------------------------------------------

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )

        # ---------------------------------------------------
        # Parse Gemini response
        # ---------------------------------------------------

        return self._parse_response(response.text)

    # -------------------------------------------------------
    # Prompt
    # -------------------------------------------------------

    def _build_prompt(
        self,
        farmer_crop: Optional[str]
    ) -> str:

        return f"""
You are an expert agricultural vision AI.

Analyze the uploaded agricultural image carefully.

Farmer provided crop:
{farmer_crop if farmer_crop else "Not Provided"}

Tasks:

1. Identify the crop visible in the image.
2. Compare the detected crop with the farmer-provided crop.
3. Assess the image quality.
4. Determine whether the crop appears healthy or diseased.
5. If diseased, identify the most likely disease.
6. Estimate the severity as mild, moderate, or severe.
7. List the visible symptoms.
8. Provide a brief explanation based only on visible evidence.
9. If the image quality is poor or the evidence is insufficient, clearly say so instead of guessing.

Important:
- Do not invent symptoms that are not visible.
- Do not make unsupported disease claims.
- If uncertain, state that the result is uncertain.
- Keep the analysis concise.

Return ONLY valid JSON.

Use exactly this structure:

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
Do not return ```json.
Do not include any text outside the JSON object.
"""

    # -------------------------------------------------------
    # Parse response
    # -------------------------------------------------------

    def _parse_response(
        self,
        response_text: str
    ) -> Dict:

        response_text = response_text.strip()

        # Remove markdown code fences if Gemini
        # happens to return them despite the instruction.
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()

        if response_text.startswith("```"):
            response_text = response_text[3:].strip()

        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()

        return json.loads(response_text)