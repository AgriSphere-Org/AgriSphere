from services.crop_planning_service import CropPlanningService


class CropPlanningAgent:

    def __init__(self):
        self.service = CropPlanningService()

    def recommend_crops(self, climate_data, soil_ph, state=None, top_n=10):
        """
        Recommend crops based on:
        - Temperature
        - Humidity
        - Rainfall
        - Soil pH
        - Region
        """

        recommendations = []

        for crop in self.service.get_all_crops():

            climate_score = self._calculate_climate_score(
                crop,
                climate_data
            )

            soil_score = self._calculate_soil_score(
                crop,
                soil_ph
            )

            region_score = self._calculate_region_score(
                crop,
                state
            )

            confidence = round(
                (climate_score * 0.5)
                + (soil_score * 0.3)
                + (region_score * 0.2),
                2
            )

            recommendations.append({
                "crop": crop["name"],
                "category": crop["category"],
                "season": crop["season"],
                "expected_profit": crop["expected_profit"],
                "water_requirement": crop["water_requirement"],
                "duration_days": crop["duration_days"],
                "confidence": confidence,
                "climate_score": climate_score,
                "soil_score": soil_score,
                "region_score": region_score,
                "suitability": self._get_suitability(confidence),
                "reasons": self._generate_reasons(
                    crop,
                    climate_score,
                    soil_score,
                    region_score
                )
            })

        recommendations.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return recommendations[:top_n]

    # --------------------------------------------------

    def _calculate_climate_score(self, crop, climate):

        score = 0

        temp = climate["temperature"]
        humidity = climate["humidity"]
        rainfall = climate["rainfall"]

        if crop["temperature"][0] <= temp <= crop["temperature"][1]:
            score += 40

        if crop["humidity"][0] <= humidity <= crop["humidity"][1]:
            score += 30

        if crop["rainfall"][0] <= rainfall <= crop["rainfall"][1]:
            score += 30

        return score

    # --------------------------------------------------

    def _calculate_soil_score(self, crop, soil_ph):

        if crop["soil_ph"][0] <= soil_ph <= crop["soil_ph"][1]:
            return 100

        difference = min(
            abs(soil_ph - crop["soil_ph"][0]),
            abs(soil_ph - crop["soil_ph"][1])
        )

        return max(30, 100 - difference * 20)

    # --------------------------------------------------

    def _calculate_region_score(self, crop, state):

        if not state:
            return 70

        if state.lower() in [
            region.lower()
            for region in crop["regions"]
        ]:
            return 100

        return 50

    # --------------------------------------------------

    def _get_suitability(self, confidence):

        if confidence >= 90:
            return "Excellent"

        if confidence >= 75:
            return "Very Good"

        if confidence >= 60:
            return "Good"

        if confidence >= 45:
            return "Moderate"

        return "Poor"

    # --------------------------------------------------

    def _generate_reasons(
        self,
        crop,
        climate_score,
        soil_score,
        region_score
    ):

        reasons = []

        if climate_score >= 80:
            reasons.append("Climate conditions are highly suitable.")

        elif climate_score >= 60:
            reasons.append("Climate conditions are acceptable.")

        else:
            reasons.append("Climate is less favorable.")

        if soil_score >= 90:
            reasons.append("Soil pH is ideal.")

        elif soil_score >= 70:
            reasons.append("Soil pH is suitable.")

        else:
            reasons.append("Soil pH needs improvement.")

        if region_score == 100:
            reasons.append("Widely cultivated in your state.")

        else:
            reasons.append("Can be cultivated with proper management.")

        return reasons