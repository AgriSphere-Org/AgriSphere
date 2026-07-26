import json
import os


class CropPlanningService:
    def __init__(self):
        self.crops = self._load_crops()

    def _load_crops(self):
        """
        Load crop knowledge base from JSON.
        """

        data_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "crops.json"
        )

        try:
            with open(data_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"Crop database not found: {data_path}")
            return []

        except json.JSONDecodeError as e:
            print(f"Invalid crops.json: {e}")
            return []

    def get_all_crops(self):
        return self.crops

    def get_crop(self, crop_name):
        for crop in self.crops:
            if crop["name"].lower() == crop_name.lower():
                return crop
        return None

    def get_crops_by_category(self, category):
        return [
            crop
            for crop in self.crops
            if crop["category"].lower() == category.lower()
        ]

    def get_crops_by_season(self, season):
        return [
            crop
            for crop in self.crops
            if season.lower() in crop["season"].lower()
        ]