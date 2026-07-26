import json
import os
from typing import List, Dict


class GovernmentSchemeService:
    """
    Government Scheme Service

    Responsibilities
    ----------------
    - Load schemes from JSON
    - Auto-detect newly added schemes
    - Return application progress
    """

    def __init__(self):

        self.scheme_file = os.path.join(
            "data",
            "government_schemes.json"
        )

        # Demo application progress
        # Later this should come from PostgreSQL
        self.application_progress = {

            "PM-KISAN": {
                "status": "Under Verification",
                "progress": 60
            },

            "Kisan Credit Card": {
                "status": "Approved",
                "progress": 100
            },

            "Pradhan Mantri Krishi Sinchai Yojana": {
                "status": "Not Applied",
                "progress": 0
            },

            "Soil Health Card Scheme": {
                "status": "Submitted",
                "progress": 40
            }

        }

    # =======================================================
    # Load Schemes
    # =======================================================

    def get_all_schemes(self) -> List[Dict]:

        if not os.path.exists(self.scheme_file):
            return []

        with open(
            self.scheme_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # =======================================================
    # Get Single Scheme
    # =======================================================

    def get_scheme(
        self,
        scheme_name: str
    ) -> Dict:

        schemes = self.get_all_schemes()

        for scheme in schemes:

            if scheme["scheme_name"].lower() == scheme_name.lower():

                return scheme

        return {}

    # =======================================================
    # Application Progress
    # =======================================================

    def get_application_progress(
        self,
        scheme_name: str
    ) -> Dict:

        return self.application_progress.get(

            scheme_name,

            {
                "status": "Not Applied",
                "progress": 0
            }

        )

    # =======================================================
    # Last Updated
    # =======================================================

    def get_last_updated(
        self,
        scheme: Dict
    ) -> str:

        return scheme.get(
            "last_updated",
            "Unknown"
        )