from typing import List, Dict


class GovernmentSchemeService:
    """
    Service responsible for managing government scheme data.

    Currently uses an in-memory database.
    Later it can be replaced with PostgreSQL.
    """

    def __init__(self):

        self.schemes = [

            {
                "scheme_name": "PM-KISAN",

                "state": "All",

                "farmer_category": [
                    "Small",
                    "Marginal",
                    "Medium"
                ],

                "minimum_land": 0,

                "maximum_land": 10,

                "supported_crops": "All",

                "irrigation": "All",

                "minimum_age": 18,

                "benefit": "₹6,000 per year",

                "official_link": "https://pmkisan.gov.in"
            },

            {
                "scheme_name": "Pradhan Mantri Krishi Sinchai Yojana",

                "state": "All",

                "farmer_category": [
                    "Small",
                    "Marginal",
                    "Medium",
                    "Large"
                ],

                "minimum_land": 0,

                "maximum_land": 100,

                "supported_crops": "All",

                "irrigation": "Drip",

                "minimum_age": 18,

                "benefit": "Subsidy on drip irrigation",

                "official_link": "https://pmksy.gov.in"
            },

            {
                "scheme_name": "Kisan Credit Card",

                "state": "All",

                "farmer_category": [
                    "Small",
                    "Marginal",
                    "Medium",
                    "Large"
                ],

                "minimum_land": 0,

                "maximum_land": 100,

                "supported_crops": "All",

                "irrigation": "All",

                "minimum_age": 18,

                "benefit": "Low-interest agricultural loan",

                "official_link": "https://www.myscheme.gov.in"
            },

            {
                "scheme_name": "Soil Health Card Scheme",

                "state": "All",

                "farmer_category": [
                    "Small",
                    "Marginal",
                    "Medium",
                    "Large"
                ],

                "minimum_land": 0,

                "maximum_land": 100,

                "supported_crops": "All",

                "irrigation": "All",

                "minimum_age": 18,

                "benefit": "Free soil testing",

                "official_link": "https://soilhealth.dac.gov.in"
            },

            {
                "scheme_name": "National Mission for Sustainable Agriculture",

                "state": "All",

                "farmer_category": [
                    "Small",
                    "Marginal"
                ],

                "minimum_land": 0,

                "maximum_land": 5,

                "supported_crops": "All",

                "irrigation": "All",

                "minimum_age": 18,

                "benefit": "Financial assistance for sustainable farming",

                "official_link": "https://nmsa.dac.gov.in"
            }

        ]

    def get_all_schemes(self) -> List[Dict]:
        """
        Returns all government schemes.
        """

        return self.schemes

    def get_scheme(self, scheme_name: str) -> Dict:
        """
        Returns details of a single scheme.
        """

        for scheme in self.schemes:

            if scheme["scheme_name"].lower() == scheme_name.lower():

                return scheme

        return {}