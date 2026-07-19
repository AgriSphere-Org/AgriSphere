from typing import Dict, List

from services.government_scheme_service import GovernmentSchemeService


class GovernmentSchemeAgent:
    """
    Government Scheme Agent

    Responsibilities:
    - Check farmer eligibility
    - Calculate confidence score
    - Rank schemes
    - Return eligible schemes
    """

    def __init__(self):

        self.scheme_service = GovernmentSchemeService()

    def recommend_schemes(

        self,

        state: str,

        farmer_category: str,

        farm_size: float,

        crop: str,

        irrigation: str,

        gender: str,

        age: int

    ) -> List[Dict]:

        schemes = self.scheme_service.get_all_schemes()

        recommendations = []

        for scheme in schemes:

            eligible = self._is_eligible(

                scheme,

                state,

                farmer_category,

                farm_size,

                crop,

                irrigation,

                gender,

                age

            )

            if eligible:

                confidence = self._calculate_confidence(

                    scheme,

                    state,

                    farmer_category,

                    farm_size,

                    crop,

                    irrigation

                )

                recommendations.append({

                    "scheme_name": scheme["scheme_name"],

                    "benefit": scheme["benefit"],

                    "official_link": scheme["official_link"],

                    "confidence": confidence

                })

        recommendations.sort(

            key=lambda x: x["confidence"],

            reverse=True

        )

        return recommendations

    # --------------------------------------------------

    def _is_eligible(

        self,

        scheme: Dict,

        state: str,

        farmer_category: str,

        farm_size: float,

        crop: str,

        irrigation: str,

        gender: str,

        age: int

    ) -> bool:

        if age < scheme["minimum_age"]:

            return False

        if scheme["state"] != "All":

            if scheme["state"].lower() != state.lower():

                return False

        if farmer_category not in scheme["farmer_category"]:

            return False

        if farm_size < scheme["minimum_land"]:

            return False

        if farm_size > scheme["maximum_land"]:

            return False

        if scheme["supported_crops"] != "All":

            if crop.lower() != scheme["supported_crops"].lower():

                return False

        if scheme["irrigation"] != "All":

            if irrigation.lower() != scheme["irrigation"].lower():

                return False

        return True

    # --------------------------------------------------

    def _calculate_confidence(

        self,

        scheme: Dict,

        state: str,

        farmer_category: str,

        farm_size: float,

        crop: str,

        irrigation: str

    ) -> int:

        score = 0

        if scheme["state"] == "All":

            score += 20

        elif scheme["state"].lower() == state.lower():

            score += 20

        if farmer_category in scheme["farmer_category"]:

            score += 20

        if scheme["minimum_land"] <= farm_size <= scheme["maximum_land"]:

            score += 20

        if scheme["supported_crops"] == "All":

            score += 20

        elif crop.lower() == scheme["supported_crops"].lower():

            score += 20

        if scheme["irrigation"] == "All":

            score += 20

        elif irrigation.lower() == scheme["irrigation"].lower():

            score += 20

        return min(score, 100)