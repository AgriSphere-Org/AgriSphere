from typing import Dict, List

from services.crop_planning_service import CropPlanningService


class CropPlanningAgent:
    """
    Crop Planning Agent

    Responsibilities:
    - Analyze climate suitability
    - Analyze soil suitability
    - Calculate confidence score
    - Recommend the best crops
    """

    def __init__(self):

        self.crop_service = CropPlanningService()

    def recommend_crop(
        self,
        temperature: float,
        humidity: float,
        rainfall: float,
        soil_ph: float
    ) -> List[Dict]:

        crops = self.crop_service.get_all_crops()

        recommendations = []

        for crop in crops:

            climate_score = self._calculate_climate_score(
                crop,
                temperature,
                humidity,
                rainfall
            )

            soil_score = self._calculate_soil_score(
                crop,
                soil_ph
            )

            confidence = round(
                (climate_score + soil_score) / 2
            )

            recommendations.append({

                "crop": crop["name"],

                "season": crop["season"],

                "expected_profit": crop["expected_profit"],

                "climate_score": climate_score,

                "soil_score": soil_score,

                "confidence": confidence

            })

        recommendations.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return recommendations[:3]

    # -------------------------------------------------

    def _calculate_climate_score(

        self,

        crop: Dict,

        temperature: float,

        humidity: float,

        rainfall: float

    ) -> int:

        score = 0

        temp_min, temp_max = crop["temperature"]

        hum_min, hum_max = crop["humidity"]

        rain_min, rain_max = crop["rainfall"]

        if temp_min <= temperature <= temp_max:

            score += 40

        if hum_min <= humidity <= hum_max:

            score += 30

        if rain_min <= rainfall <= rain_max:

            score += 30

        return score

    # -------------------------------------------------

    def _calculate_soil_score(

        self,

        crop: Dict,

        soil_ph: float

    ) -> int:

        ph_min, ph_max = crop["soil_ph"]

        if ph_min <= soil_ph <= ph_max:

            return 100

        return 40