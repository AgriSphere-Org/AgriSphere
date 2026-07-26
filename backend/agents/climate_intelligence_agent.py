import logging
from typing import Dict, Any

from services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class ClimateAgent:

    def __init__(self):
        self.weather_service = WeatherService()

    # ==========================================================
    # Main Analysis
    # ==========================================================

    def analyze(
        self,
        state: str,
        district: str,
        crop: str,
        village: str = None
    ) -> Dict[str, Any]:

        # ------------------------------------------
        # Current Weather
        # ------------------------------------------

        current = self.weather_service.get_current_weather(
            state,
            district,
            village
        )

        # ------------------------------------------
        # Forecast
        # ------------------------------------------

        forecast = self.weather_service.get_forecast(
            state,
            district,
            village
        )

        # ------------------------------------------
        # Extract Weather
        # ------------------------------------------

        main = current.get("main", {})
        wind = current.get("wind", {})
        rain = current.get("rain", {})
        weather = current.get("weather", [{}])

        temperature = main.get("temp", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)

        rainfall = rain.get("1h", rain.get("3h", 0))

        weather_condition = weather[0].get("main", "Unknown")

        # ------------------------------------------
        # Climate Risks
        # ------------------------------------------

        heat_stress = self._heat_stress(temperature)

        drought_risk = self._drought_risk(
            temperature,
            humidity,
            rainfall
        )

        flood_risk = self._flood_risk(
            rainfall,
            humidity
        )

        farming_condition = self._farming_condition(
            temperature,
            humidity,
            rainfall
        )

        # ------------------------------------------
        # Crop Advisory
        # ------------------------------------------

        recommendation = self._recommendation(
            crop,
            farming_condition,
            heat_stress,
            drought_risk,
            flood_risk
        )

        irrigation = self._irrigation_advice(
            rainfall,
            temperature
        )

        disease = self._disease_risk(
            humidity,
            rainfall
        )

        # ------------------------------------------
        # Graph Analytics
        # ------------------------------------------

        analytics = self.weather_service.build_weather_analytics(
            forecast
        )

        analytics = self.weather_service.calculate_crop_stress(
            analytics
        )

        analytics = self.weather_service.calculate_irrigation_index(
            analytics
        )

        logger.info(
            f"Climate analysis completed for {district}, {state}"
        )

        location = (
            f"{district}, {state}"
            if village is None
            else f"{village}, {district}, {state}"
        )

        return {

            "location": location,

            "crop": crop,

            "current_weather": {

                "temperature": temperature,

                "humidity": humidity,

                "rainfall": rainfall,

                "wind_speed": wind_speed,

                "weather": weather_condition

            },

            "advisory": {

                "farming_condition": farming_condition,

                "recommendation": recommendation,

                "irrigation_advice": irrigation,

                "disease_risk": disease,

                "heat_stress": heat_stress,

                "drought_risk": drought_risk,

                "flood_risk": flood_risk

            },

            "analytics": analytics

        }

    # ==========================================================
    # Heat Stress
    # ==========================================================

    def _heat_stress(self, temperature):

        if temperature >= 40:
            return "Very High"

        if temperature >= 35:
            return "High"

        if temperature >= 30:
            return "Moderate"

        return "Low"

    # ==========================================================

    def _drought_risk(
        self,
        temperature,
        humidity,
        rainfall
    ):

        if rainfall < 2 and humidity < 35 and temperature > 35:
            return "High"

        if rainfall < 5 and humidity < 50:
            return "Moderate"

        return "Low"

    # ==========================================================

    def _flood_risk(
        self,
        rainfall,
        humidity
    ):

        if rainfall > 30:
            return "High"

        if rainfall > 10:
            return "Moderate"

        if humidity > 90:
            return "Moderate"

        return "Low"

    # ==========================================================

    def _farming_condition(
        self,
        temperature,
        humidity,
        rainfall
    ):

        if 20 <= temperature <= 30 and 45 <= humidity <= 75:
            return "Excellent"

        if 18 <= temperature <= 35:
            return "Good"

        if rainfall > 40:
            return "Poor"

        return "Average"

    # ==========================================================
    # Recommendation
    # ==========================================================

    def _recommendation(
        self,
        crop,
        farming_condition,
        heat_stress,
        drought_risk,
        flood_risk
    ):

        if flood_risk == "High":
            return (
                f"Heavy rainfall is expected. Ensure proper drainage in the {crop} field and avoid fertilizer application."
            )

        if drought_risk == "High":
            return (
                f"Dry conditions are expected. Increase irrigation and conserve soil moisture for {crop}."
            )

        if heat_stress == "Very High":
            return (
                f"Extreme heat detected. Irrigate {crop} early morning or late evening."
            )

        if farming_condition == "Excellent":
            return (
                f"Current weather is highly favorable for {crop}. Continue normal farming practices."
            )

        if farming_condition == "Good":
            return (
                f"Weather conditions are suitable for {crop}. Continue regular monitoring and field activities."
            )

        return (
            f"Monitor weather conditions closely before performing major operations in the {crop} field."
        )

    # ==========================================================
    # Irrigation Advice
    # ==========================================================

    def _irrigation_advice(
        self,
        rainfall,
        temperature
    ):

        if rainfall > 15:
            return "No irrigation required."

        if temperature > 35:
            return "Increase irrigation frequency."

        if temperature < 22:
            return "Light irrigation is sufficient."

        return "Maintain regular irrigation schedule."

    # ==========================================================
    # Disease Risk
    # ==========================================================

    def _disease_risk(
        self,
        humidity,
        rainfall
    ):

        if humidity > 85 and rainfall > 5:
            return "High"

        if humidity > 70:
            return "Moderate"

        return "Low"