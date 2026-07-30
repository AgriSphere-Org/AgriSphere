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
                "unit": "Quintal",
                "price_history": [
                    2350, 2380, 2400, 2420, 2440, 2460,
                    2480, 2500, 2530, 2570, 2610, 2650
                ],
                "price_prediction": [
                    2670, 2690, 2720, 2750, 2780, 2810,
                    2840, 2870, 2900, 2930, 2960, 3000
                ]
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
                "unit": "Quintal",
                "price_history": [
                    2200, 2220, 2240, 2260, 2280, 2300,
                    2320, 2350, 2380, 2400, 2430, 2450
                ],
                "price_prediction": [
                    2470, 2490, 2510, 2530, 2550, 2570,
                    2590, 2610, 2630, 2650, 2670, 2700
                ]
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
                "unit": "Quintal",
                "price_history": [
                    2450, 2500, 2550, 2620, 2700, 2780,
                    2850, 2920, 3000, 3080, 3150, 3200
                ],
                "price_prediction": [
                    3250, 3300, 3350, 3400, 3450, 3500,
                    3550, 3600, 3650, 3700, 3750, 3800
                ]
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
                "unit": "Quintal",
                "price_history": [
                    6700, 6750, 6800, 6840, 6880, 6920,
                    6960, 7000, 7050, 7100, 7150, 7200
                ],
                "price_prediction": [
                    7250, 7300, 7350, 7400, 7450, 7500,
                    7550, 7600, 7650, 7700, 7750, 7800
                ]
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
                "unit": "Quintal",
                "price_history": [
                    4400, 4440, 4480, 4520, 4560, 4600,
                    4650, 4700, 4740, 4780, 4820, 4850
                ],
                "price_prediction": [
                    4880, 4920, 4960, 5000, 5040, 5080,
                    5120, 5160, 5200, 5240, 5280, 5320
                ]
            }
        ]

    def get_all_market_data(self) -> List[Dict]:
        """Returns complete market dataset."""
        return self.market_data

    def get_market_data(self, crop: str, state: str, district: str) -> Dict:
        """Returns market information for a crop based on crop, state, and district."""
        for market in self.market_data:
            if (
                market["crop"].lower() == crop.lower()
                and market["state"].lower() == state.lower()
                and market["district"].lower() == district.lower()
            ):
                return market
        return {}

    def get_crop(self, crop: str) -> Dict:
        """Returns market data for a crop."""
        for market in self.market_data:
            if market["crop"].lower() == crop.lower():
                return market
        return {}

    def compare_crops(self, crop1: str, crop2: str) -> Dict:
        """Returns data for comparison of two crops."""
        crop_one = self.get_crop(crop1)
        crop_two = self.get_crop(crop2)

        return {
            "crop1": crop_one,
            "crop2": crop_two
        }