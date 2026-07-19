import logging
from typing import Dict, Any

from services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class ClimateAgent:
    """
    Climate Intelligence Agent

    Responsibilities:
    - Analyze current weather
    - Assess farming conditions
    - Detect heat stress
    - Detect drought risk
    - Detect flood risk
    - Generate agricultural recommendations
    """

    def __init__(self):
        self.weather_service = WeatherService()

    def analyze(self, city: str) -> Dict[str, Any]:
        """
        Main function that performs climate analysis.
        """

        current = self.weather_service.get_current_weather(city)
        try:
            forecast = self.weather_service.get_forecast(city)
        except Exception:
            forecast = {}

        main = current.get("main", {})
        wind = current.get("wind", {})
        rain = current.get("rain", {})

        temperature = main.get("temp", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)

        rainfall = 0

        if "1h" in rain:
            rainfall = rain["1h"]

        elif "3h" in rain:
            rainfall = rain["3h"]

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

        recommendation = self._recommendation(
            farming_condition,
            heat_stress,
            drought_risk,
            flood_risk
        )

        logger.info(f"Climate analysis completed for {city}")

        return {

            "location": city,

            "temperature": temperature,

            "humidity": humidity,

            "rainfall": rainfall,

            "wind_speed": wind_speed,

            "heat_stress": heat_stress,

            "drought_risk": drought_risk,

            "flood_risk": flood_risk,

            "farming_condition": farming_condition,

            "recommendation": recommendation,

            "forecast": forecast

        }

    # --------------------------------------------------------

    def _heat_stress(self, temperature: float) -> str:

        if temperature >= 40:
            return "Very High"

        elif temperature >= 35:
            return "High"

        elif temperature >= 30:
            return "Moderate"

        return "Low"

    # --------------------------------------------------------

    def _drought_risk(
        self,
        temperature: float,
        humidity: float,
        rainfall: float
    ) -> str:

        if rainfall < 2 and humidity < 35 and temperature > 35:
            return "High"

        elif rainfall < 5 and humidity < 50:
            return "Moderate"

        return "Low"

    # --------------------------------------------------------

    def _flood_risk(
        self,
        rainfall: float,
        humidity: float
    ) -> str:

        if rainfall > 30:
            return "High"

        elif rainfall > 10:
            return "Moderate"

        elif humidity > 90:
            return "Moderate"

        return "Low"

    # --------------------------------------------------------

    def _farming_condition(
        self,
        temperature: float,
        humidity: float,
        rainfall: float
    ) -> str:

        if 20 <= temperature <= 30 and 45 <= humidity <= 75:
            return "Excellent"

        elif 18 <= temperature <= 35:
            return "Good"

        elif rainfall > 40:
            return "Poor"

        return "Average"

    # --------------------------------------------------------

    def _recommendation(
        self,
        farming_condition: str,
        heat_stress: str,
        drought_risk: str,
        flood_risk: str
    ) -> str:

        if flood_risk == "High":
            return (
                "Heavy rainfall expected. Improve field drainage and avoid sowing."
            )

        if drought_risk == "High":
            return (
                "Water scarcity likely. Increase irrigation and conserve moisture."
            )

        if heat_stress == "Very High":
            return (
                "Extreme heat detected. Irrigate during early morning or evening."
            )

        if farming_condition == "Excellent":
            return (
                "Weather conditions are highly favorable for farming activities."
            )

        if farming_condition == "Good":
            return (
                "Suitable conditions for cultivation. Continue routine monitoring."
            )

        return (
            "Monitor weather regularly before making agricultural decisions."
        )