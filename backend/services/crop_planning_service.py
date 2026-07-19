from typing import Dict, List


class CropPlanningService:
    """
    Service responsible for providing crop information.
    Later this can be replaced with a database or ML model.
    """

    def __init__(self):

        self.crops = [

            {
                "name": "Rice",
                "season": "Kharif",
                "temperature": (20, 35),
                "humidity": (70, 100),
                "rainfall": (100, 300),
                "soil_ph": (5.5, 7.0),
                "expected_profit": "₹90,000 - ₹1,20,000"
            },

            {
                "name": "Wheat",
                "season": "Rabi",
                "temperature": (10, 25),
                "humidity": (40, 70),
                "rainfall": (30, 100),
                "soil_ph": (6.0, 7.5),
                "expected_profit": "₹60,000 - ₹90,000"
            },

            {
                "name": "Maize",
                "season": "Kharif",
                "temperature": (18, 30),
                "humidity": (50, 80),
                "rainfall": (50, 150),
                "soil_ph": (5.5, 7.5),
                "expected_profit": "₹70,000 - ₹1,00,000"
            },

            {
                "name": "Cotton",
                "season": "Kharif",
                "temperature": (25, 38),
                "humidity": (40, 70),
                "rainfall": (50, 120),
                "soil_ph": (5.8, 8.0),
                "expected_profit": "₹1,00,000 - ₹1,50,000"
            },

            {
                "name": "Sugarcane",
                "season": "Annual",
                "temperature": (20, 35),
                "humidity": (60, 90),
                "rainfall": (100, 250),
                "soil_ph": (6.0, 7.8),
                "expected_profit": "₹1,50,000 - ₹2,20,000"
            },

            {
                "name": "Soybean",
                "season": "Kharif",
                "temperature": (20, 30),
                "humidity": (50, 80),
                "rainfall": (60, 150),
                "soil_ph": (6.0, 7.5),
                "expected_profit": "₹80,000 - ₹1,10,000"
            }

        ]

    def get_all_crops(self) -> List[Dict]:
        """
        Returns all crop information.
        """

        return self.crops

    def get_crop(self, crop_name: str) -> Dict:
        """
        Returns details of a specific crop.
        """

        for crop in self.crops:

            if crop["name"].lower() == crop_name.lower():

                return crop

        return {}