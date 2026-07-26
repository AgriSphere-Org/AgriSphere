from typing import Dict, List

from services.government_scheme_service import GovernmentSchemeService


class GovernmentSchemeAgent:

    def __init__(self):
        self.scheme_service = GovernmentSchemeService()

    # =====================================================
    # Recommend Schemes
    # =====================================================

    def recommend_schemes(
        self,
        state: str,
        farmer_category: str,
        purpose: str
    ) -> List[Dict]:

        schemes = self.scheme_service.get_all_schemes()

        recommendations = []

        for scheme in schemes:

            confidence = self._calculate_confidence(
                scheme,
                state,
                farmer_category,
                purpose
            )

            if confidence >= 40:

                progress = self.scheme_service.get_application_progress(
                    scheme["scheme_name"]
                )

                recommendations.append({

                    "scheme_name":
                        scheme["scheme_name"],

                    "description":
                        scheme.get(
                            "description",
                            ""
                        ),

                    "benefit":
                        scheme["benefit"],

                    "eligibility":
                        "Eligible",

                    "application_status":
                        progress["status"],

                    "progress_percentage":
                        progress["progress"],

                    "official_apply_url":
                        scheme["official_apply_url"],

                    "last_updated":
                        self.scheme_service.get_last_updated(
                            scheme
                        ),

                    "confidence":
                        confidence

                })

        recommendations.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return recommendations

    # =====================================================
    # Confidence Score
    # =====================================================

    def _calculate_confidence(
        self,
        scheme: Dict,
        state: str,
        farmer_category: str,
        purpose: str
    ) -> int:

        score = 0

        # ------------------------------
        # State Match
        # ------------------------------

        scheme_states = [
            s.lower()
            for s in scheme.get("state", [])
        ]

        if "all" in scheme_states:
            score += 30

        elif state.lower() in scheme_states:
            score += 30

        # ------------------------------
        # Farmer Category
        # ------------------------------

        categories = [
            c.lower()
            for c in scheme.get(
                "farmer_category",
                []
            )
        ]

        if farmer_category.lower() in categories:
            score += 35

        # ------------------------------
        # Purpose
        # ------------------------------

        purposes = [
            p.lower()
            for p in scheme.get(
                "purpose",
                []
            )
        ]

        if purpose.lower() in purposes:
            score += 35

        return min(score, 100)