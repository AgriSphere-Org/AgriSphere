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

        irrigation = self._irrigation_advice(

            climate_data

        )

        fertilizer = self._fertilizer_advice(

            crop_health

        )

        disease = self._disease_prevention(

            crop_health

        )

        harvest = self._harvest_advice(

            climate_data,

            crop_health

        )

        selling = self._selling_advice(

            market_data

        )

        risk = self._overall_risk(

            climate_data,

            crop_health

        )

        overall = self._overall_summary(

            risk,

            crop_health,

            market_data

        )

        return {

            "recommended_crop":

                crop_plan["crop"],

            "recommended_season":

                crop_plan["season"],

            "irrigation_advice":

                irrigation,

            "fertilizer_advice":

                fertilizer,

            "disease_prevention":

                disease,

            "harvest_recommendation":

                harvest,

            "selling_recommendation":

                selling,

            "government_schemes":[

                scheme["scheme_name"]

                for scheme in government_schemes

            ],

            "overall_risk":

                risk,

            "overall_summary":

                overall

        }

    # --------------------------------------------------------

    def _irrigation_advice(

        self,

        climate: Dict

    ) -> str:

        if climate["drought_risk"] == "High":

            return "Increase irrigation frequency."

        if climate["flood_risk"] == "High":

            return "Reduce irrigation and improve drainage."

        return "Maintain regular irrigation schedule."

    # --------------------------------------------------------

    def _fertilizer_advice(

        self,

        crop_health: Dict

    ) -> str:

        if crop_health["health_score"] >= 90:

            return "Continue balanced NPK fertilizer."

        if crop_health["health_score"] >= 70:

            return "Apply micronutrient supplements."

        return "Consult soil testing before applying fertilizer."

    # --------------------------------------------------------

    def _disease_prevention(

        self,

        crop_health: Dict

    ) -> str:

        if crop_health["severity"] == "Severe":

            return "Immediate treatment required."

        if crop_health["severity"] == "Moderate":

            return "Monitor crop and begin preventive spraying."

        return "Continue routine monitoring."

    # --------------------------------------------------------

    def _harvest_advice(

        self,

        climate: Dict,

        crop_health: Dict

    ) -> str:

        if climate["flood_risk"] == "High":

            return "Harvest as early as possible."

        if crop_health["severity"] == "Severe":

            return "Prioritize harvesting healthy crops."

        return "Harvest according to crop maturity."

    # --------------------------------------------------------

    def _selling_advice(

        self,

        market: Dict

    ) -> str:

        trend = market["market_trend"]

        if trend == "Strongly Increasing":

            return "Wait before selling."

        if trend == "Increasing":

            return "Selling after a few days may increase profit."

        if trend == "Stable":

            return "Current market is suitable for selling."

        return "Consider selling soon."

    # --------------------------------------------------------

    def _overall_risk(

        self,

        climate: Dict,

        crop_health: Dict

    ) -> str:

        if (

            climate["flood_risk"] == "High"

            or

            climate["drought_risk"] == "High"

            or

            crop_health["severity"] == "Severe"

        ):

            return "High"

        if (

            crop_health["severity"] == "Moderate"

            or

            climate["heat_stress"] == "High"

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

        if risk == "High":

            return (

                "Immediate intervention is recommended "

                "to reduce crop losses."

            )

        if (

            market["market_trend"]

            in [

                "Increasing",

                "Strongly Increasing"

            ]

            and

            crop_health["health_score"] >= 90

        ):

            return (

                "Excellent farming conditions with "

                "strong market opportunities."

            )

        return (

            "Continue regular monitoring "

            "and follow recommended practices."

        )