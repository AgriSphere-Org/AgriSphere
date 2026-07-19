from typing import Dict

from PIL import Image

from services.disease_detection_service import DiseaseDetectionService


class CropHealthAgent:

    def __init__(self):

        self.disease_service = DiseaseDetectionService()

    # -------------------------------------------------------

    def analyze_crop(self, image_path: str) -> Dict:

        # Open image using Pillow
        image = Image.open(image_path)

        prediction = self.disease_service.predict(image)

        disease = prediction["disease"]

        confidence = prediction["confidence"]

        health_score = self._calculate_health_score(
            disease,
            confidence
        )

        severity = self._calculate_severity(
            disease,
            confidence
        )

        recommendation = self._generate_recommendation(
            disease,
            severity
        )

        return {

            "crop": prediction.get("crop", "Unknown"),

            "disease": disease,

            "confidence": confidence,

            "health_score": health_score,

            "severity": severity,

            "recommendation": recommendation

        }

    # -------------------------------------------------------

    def _calculate_health_score(
        self,
        disease: str,
        confidence: float
    ) -> int:

        if disease.lower() == "healthy":
            return 100

        score = int(100 - confidence)

        return max(score, 10)

    # -------------------------------------------------------

    def _calculate_severity(
        self,
        disease: str,
        confidence: float
    ) -> str:

        if disease.lower() == "healthy":
            return "None"

        if confidence >= 95:
            return "Severe"

        elif confidence >= 80:
            return "Moderate"

        elif confidence >= 60:
            return "Mild"

        return "Low"

    # -------------------------------------------------------

    def _generate_recommendation(
        self,
        disease: str,
        severity: str
    ) -> str:

        if disease.lower() == "healthy":

            return "Crop appears healthy. Continue regular monitoring."

        recommendations = {

            "Leaf Blight":
                "Apply recommended fungicide and remove infected leaves.",

            "Powdery Mildew":
                "Use sulfur-based fungicide and improve air circulation.",

            "Bacterial Spot":
                "Avoid overhead irrigation and use copper-based sprays.",

            "Rust":
                "Apply appropriate fungicide and remove infected foliage.",

            "Early Blight":
                "Use crop rotation and fungicide treatment.",

            "Late Blight":
                "Remove infected plants immediately and spray fungicide."

        }

        return recommendations.get(

            disease,

            "Consult your nearest agricultural extension officer."

        )