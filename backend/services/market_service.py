from typing import Dict, List


class MarketService:
    """
    Service responsible for fetching market data.

    Currently uses an in-memory database.
    Later this can be replaced with:
    - AGMARKNET API
    - eNAM API
    - PostgreSQL
    """

    def __init__(self):

        self.market_data = [

            {
                "crop": "Rice",

                "state": "Maharashtra",

                "district": "Nagpur",

                "market": "Nagpur APMC",

                "current_price": 2650,

                "average_price": 2480,

                "minimum_price": 2350,

                "maximum_price": 2780,

                "arrival_quantity": 350,

                "unit": "Quintal"

            },

            {
                "crop": "Wheat",

                "state": "Maharashtra",

                "district": "Nashik",

                "market": "Nashik APMC",

                "current_price": 2450,

                "average_price": 2300,

                "minimum_price": 2200,

                "maximum_price": 2550,

                "arrival_quantity": 420,

                "unit": "Quintal"

            },

            {
                "crop": "Tomato",

                "state": "Maharashtra",

                "district": "Pune",

                "market": "Pune APMC",

                "current_price": 3200,

                "average_price": 2850,

                "minimum_price": 2500,

                "maximum_price": 3400,

                "arrival_quantity": 180,

                "unit": "Quintal"

            },

            {
                "crop": "Cotton",

                "state": "Maharashtra",

                "district": "Akola",

                "market": "Akola APMC",

                "current_price": 7200,

                "average_price": 6900,

                "minimum_price": 6700,

                "maximum_price": 7450,

                "arrival_quantity": 240,

                "unit": "Quintal"

            },

            {
                "crop": "Soybean",

                "state": "Maharashtra",

                "district": "Latur",

                "market": "Latur APMC",

                "current_price": 4850,

                "average_price": 4600,

                "minimum_price": 4400,

                "maximum_price": 5000,

                "arrival_quantity": 270,

                "unit": "Quintal"

            }

        ]

    # ------------------------------------------------------

    def get_all_market_data(self) -> List[Dict]:
        """
        Returns complete market dataset.
        """

        return self.market_data

    # ------------------------------------------------------

    def get_market_data(

        self,

        crop: str,

        state: str,

        district: str

    ) -> Dict:
        """
        Returns market information
        for a crop.
        """

        for market in self.market_data:

            if (

                market["crop"].lower() == crop.lower()

                and

                market["state"].lower() == state.lower()

                and

                market["district"].lower() == district.lower()

            ):

                return market

        return {}