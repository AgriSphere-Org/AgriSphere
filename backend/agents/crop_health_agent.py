from typing import Dict

from PIL import Image

from services.gemini_vision_service import GeminiVisionService


class CropHealthAgent:
    """
    Crop Health Agent

    Responsibilities:
    - Receive crop image
    - Analyze using Gemini Vision
    - Calculate health score
    - Return structured crop health result
    """

    def __init__(self):

        self.vision_service = GeminiVisionService()

    # -------------------------------------------------------

    def analyze_crop(
        self,
        crop: str,
        image_path: str
    ) -> Dict:

        image = Image.open(image_path)

        analysis = self.vision_service.analyze_crop(
            image=image,
            farmer_crop=crop
        )

        health_score = self._calculate_health_score(
            analysis["health_status"],
            analysis["severity"]
        )

        return {

            "crop": crop if crop else "Unknown",

            "detected_crop":
                analysis.get(
                    "detected_crop",
                    "Unknown"
                ),

            "crop_match":
                analysis.get(
                    "crop_match",
                    False
                ),

            "image_quality":
                analysis.get(
                    "image_quality",
                    "Unknown"
                ),

            "health_status":
                analysis.get(
                    "health_status",
                    "Unknown"
                ),

            "disease":
                analysis.get(
                    "disease",
                    None
                ),

            "health_score":
                health_score,

            "severity":
                analysis.get(
                    "severity",
                    "Unknown"
                ),

            "visible_symptoms":
                analysis.get(
                    "visible_symptoms",
                    []
                ),

            "analysis_summary":
                analysis.get(
                    "analysis_summary",
                    ""
                )
        }

    # -------------------------------------------------------

    def _calculate_health_score(
        self,
        health_status: str,
        severity: str
    ) -> int:

        if health_status.lower() == "healthy":
            return 100

        severity_scores = {

            "mild": 80,

            "moderate": 60,

            "severe": 35

        }

        return severity_scores.get(
            severity.lower(),
            50
        )