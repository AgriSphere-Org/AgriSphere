import os
from typing import Dict, List, Optional, Union

import numpy as np
from PIL import Image

# Uncomment these if you have TensorFlow installed
# from tensorflow.keras.models import load_model


class DiseaseDetectionService:
    """
    Service responsible for loading the disease detection model
    and predicting crop diseases from leaf images.
    """

    def __init__(self):

        self.model = None

        self.image_size = (224, 224)

        # Replace with your actual model path
        self.model_path = "models/crop_disease_model.h5"

        self.class_names = [

            "Healthy",

            "Bacterial Spot",

            "Early Blight",

            "Late Blight",

            "Leaf Mold",

            "Powdery Mildew",

            "Rust",

            "Septoria Leaf Spot"

        ]

        # 1. Added in-memory dictionary for history tracking
        self.crop_history: Dict[str, List[Dict]] = {}

        self.load_model()

    # --------------------------------------------------------

    def load_model(self):

        """
        Loads the trained model.

        Currently placeholder.
        """

        if os.path.exists(self.model_path):

            try:

                # Uncomment after adding TensorFlow

                # self.model = load_model(self.model_path)

                self.model = "MODEL_LOADED"

                print("Disease detection model loaded successfully.")

            except Exception as e:

                print(f"Error loading model: {e}")

                self.model = None

        else:

            print("Model file not found.")

            self.model = None

    # --------------------------------------------------------

    def preprocess_image(

        self,

        image: Image.Image

    ) -> np.ndarray:

        """
        Resize and normalize image.
        """

        image = image.convert("RGB")

        image = image.resize(self.image_size)

        image = np.array(image)

        image = image.astype("float32") / 255.0

        image = np.expand_dims(image, axis=0)

        return image

    # --------------------------------------------------------

    def predict(

        self,

        image: Image.Image

    ) -> Dict:

        """
        Predict disease.

        Placeholder implementation.
        """

        processed = self.preprocess_image(image)

        # Replace with actual prediction later

        disease = "Healthy"

        confidence = 96.7

        severity = "None"

        health_score = 98

        # 2. Included status based on disease value
        status = "Healthy" if disease == "Healthy" else "Diseased"

        return {

            "disease": disease,

            "confidence": confidence,

            "severity": severity,

            "health_score": health_score,

            "status": status

        }

    # --------------------------------------------------------

    def is_model_loaded(self) -> bool:

        return self.model is not None

    # --------------------------------------------------------
    # NEW METHODS ADDED BELOW
    # --------------------------------------------------------

    def save_history(self, crop: str, result: Dict) -> None:
        """
        Store prediction result in memory for a specific crop.
        """
        if crop not in self.crop_history:
            self.crop_history[crop] = []
        self.crop_history[crop].append(result)

    def get_crop_history(self, crop: str) -> List[Dict]:
        """
        Return the complete prediction history list for a specific crop.
        """
        return self.crop_history.get(crop, [])

    def compare_health(self, crop: str) -> Dict[str, Union[Optional[int], Optional[float], str]]:
        """
        Compare latest and previous health scores for a crop.
        Returns previous_score, current_score, difference, and trend.
        """
        history = self.get_crop_history(crop)

        if len(history) < 2:
            current_score = history[-1].get("health_score") if history else None
            return {
                "previous_score": None,
                "current_score": current_score,
                "difference": 0,
                "trend": "Insufficient Data"
            }

        previous_score = history[-2].get("health_score")
        current_score = history[-1].get("health_score")
        difference = current_score - previous_score

        if difference > 0:
            trend = "Improved"
        elif difference < 0:
            trend = "Declined"
        else:
            trend = "Stable"

        return {
            "previous_score": previous_score,
            "current_score": current_score,
            "difference": difference,
            "trend": trend
        }

    def generate_graph_data(self, crop: str) -> List[int]:
        """
        Return a list containing only the health_score values recorded for the crop.
        """
        history = self.get_crop_history(crop)
        return [item["health_score"] for item in history if "health_score" in item]