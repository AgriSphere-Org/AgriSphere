from typing import Dict, List


class RecommendationAgent:
    """
    Recommendation Agent

    Responsibilities:
    - Combine outputs from all agents
    - Analyze overall farm condition
    - Calculate overall risk
    - Generate actionable recommendations
    """

    def generate_recommendation(
        self,
        climate_data: Dict,
        crop_plan: Dict,
        crop_health: Dict,
        market_data: Dict,
        government_schemes: List[Dict]
    ) -> Dict:

        irrigation = self._irrigation_advice(climate_data)
        fertilizer = self._fertilizer_advice(crop_health)
        disease = self._disease_prevention(crop_health)
        harvest = self._harvest_advice(climate_data, crop_health)
        selling = self._selling_advice(market_data)
        risk = self._overall_risk(climate_data, crop_health)
        overall = self._overall_summary(risk, crop_health, market_data)

        schemes_list = [
            scheme.get("scheme_name", "Unknown Scheme")
            for scheme in (government_schemes or [])
            if isinstance(scheme, dict)
        ]

        crop_name = (
    crop_plan.get("recommended_crop")
    or crop_plan.get("crop")
    or "Unknown Crop"
)
        season_name = crop_plan.get("season", "Current Season")

        ai_report = self._generate_ai_report(
            crop_name=crop_name,
            season_name=season_name,
            risk=risk,
            irrigation=irrigation,
            fertilizer=fertilizer,
            disease=disease,
            selling=selling,
            overall=overall
        )

        return {
            "recommended_crop": crop_name,
            "recommended_season": season_name,
            "irrigation_advice": irrigation,
            "fertilizer_advice": fertilizer,
            "disease_prevention": disease,
            "harvest_recommendation": harvest,
            "selling_recommendation": selling,
            "government_schemes": schemes_list,
            "overall_risk": risk,
            "overall_summary": overall,
            "ai_report": ai_report
        }

    # --------------------------------------------------------

    def _irrigation_advice(self, climate: Dict) -> str:
        drought_risk = climate.get("drought_risk", "Low")
        flood_risk = climate.get("flood_risk", "Low")

        if drought_risk == "High":
            return "Increase irrigation frequency."
        if flood_risk == "High":
            return "Reduce irrigation and improve drainage."
        return "Maintain regular irrigation schedule."

    # --------------------------------------------------------

    def _fertilizer_advice(self, crop_health: Dict) -> str:
        health_score = crop_health.get("health_score", 100)

        if health_score >= 90:
            return "Continue balanced NPK fertilizer."
        if health_score >= 70:
            return "Apply micronutrient supplements."
        return "Consult soil testing before applying fertilizer."

    # --------------------------------------------------------

    def _disease_prevention(self, crop_health: Dict) -> str:
        severity = crop_health.get("severity", "None")

        if severity == "Severe":
            return "Immediate treatment required."
        if severity == "Moderate":
            return "Monitor crop and begin preventive spraying."
        return "Continue routine monitoring."

    # --------------------------------------------------------

    def _harvest_advice(self, climate: Dict, crop_health: Dict) -> str:
        flood_risk = climate.get("flood_risk", "Low")
        severity = crop_health.get("severity", "None")

        if flood_risk == "High":
            return "Harvest as early as possible."
        if severity == "Severe":
            return "Prioritize harvesting healthy crops."
        return "Harvest according to crop maturity."

    # --------------------------------------------------------

    def _selling_advice(self, market: Dict) -> str:
        trend = market.get("market_trend", "Stable")

        if trend == "Strongly Increasing":
            return "Wait before selling."
        if trend == "Increasing":
            return "Selling after a few days may increase profit."
        if trend == "Stable":
            return "Current market is suitable for selling."
        return "Consider selling soon."

    # --------------------------------------------------------

    def _overall_risk(self, climate: Dict, crop_health: Dict) -> str:
        flood_risk = climate.get("flood_risk", "Low")
        drought_risk = climate.get("drought_risk", "Low")
        heat_stress = climate.get("heat_stress", "Low")
        severity = crop_health.get("severity", "None")

        if (
            flood_risk == "High"
            or drought_risk == "High"
            or severity == "Severe"
        ):
            return "High"

        if (
            severity == "Moderate"
            or heat_stress == "High"
        ):
            return "Moderate"

        return "Low"

    # --------------------------------------------------------

    def _overall_summary(
        self,
        risk: str,
        crop_health: Dict,
        market: Dict
    ) -> str:
        market_trend = market.get("market_trend", "Stable")
        health_score = crop_health.get("health_score", 100)

        if risk == "High":
            return (
                "Immediate intervention is recommended "
                "to reduce crop losses."
            )

        if (
            market_trend in ["Increasing", "Strongly Increasing"]
            and health_score >= 90
        ):
            return (
                "Excellent farming conditions with "
                "strong market opportunities."
            )

        return (
            "Continue regular monitoring "
            "and follow recommended practices."
        )

    # --------------------------------------------------------

    def _generate_ai_report(
        self,
        crop_name: str,
        season_name: str,
        risk: str,
        irrigation: str,
        fertilizer: str,
        disease: str,
        selling: str,
        overall: str
    ) -> str:
        return (
            f"AgriSphere Recommendation Report for {crop_name} ({season_name}):\n"
            f"- Overall Risk Level: {risk}\n"
            f"- Summary: {overall}\n"
            f"- Action Plan:\n"
            f"  1. Irrigation: {irrigation}\n"
            f"  2. Soil & Nutrition: {fertilizer}\n"
            f"  3. Crop Protection: {disease}\n"
            f"  4. Market Strategy: {selling}"
        )