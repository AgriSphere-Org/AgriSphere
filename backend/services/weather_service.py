import logging
from typing import Dict, Any, Optional

import requests

from config.settings import WEATHER_API_KEY

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Handles communication with OpenWeather API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):

        if not WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is missing.")

        self.api_key = WEATHER_API_KEY

    # ==========================================================
    # Build Location Query
    # ==========================================================

    def _build_location_query(
        self,
        state: str,
        district: str,
        village: Optional[str] = None
    ) -> str:

        if village:
            return f"{village},{district},{state},IN"

        return f"{district},{state},IN"

    # ==========================================================
    # Current Weather
    # ==========================================================

    def get_current_weather(
        self,
        state: str,
        district: str,
        village: Optional[str] = None
    ) -> Dict[str, Any]:

        query = self._build_location_query(
            state,
            district,
            village
        )

        endpoint = f"{self.BASE_URL}/weather"

        params = {
            "q": query,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(
            endpoint,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        logger.info(f"Current weather fetched for {query}")

        return response.json()

    # ==========================================================
    # Forecast
    # ==========================================================

    def get_forecast(
        self,
        state: str,
        district: str,
        village: Optional[str] = None
    ) -> Dict[str, Any]:

        query = self._build_location_query(
            state,
            district,
            village
        )

        endpoint = f"{self.BASE_URL}/forecast"

        params = {
            "q": query,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(
            endpoint,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        logger.info(f"Forecast fetched for {query}")

        return response.json()

    # ==========================================================
    # Weather Analytics
    # ==========================================================

    def build_weather_analytics(
        self,
        forecast: Dict[str, Any]
    ) -> Dict[str, Any]:

        dates = []
        temperature = []
        humidity = []
        rainfall = []
        wind = []

        for item in forecast.get("list", [])[:10]:

            dates.append(item["dt_txt"])

            temperature.append(item["main"]["temp"])

            humidity.append(item["main"]["humidity"])

            rainfall.append(
                item.get("rain", {}).get("3h", 0)
            )

            wind.append(item["wind"]["speed"])

        return {

            "dates": dates,

            "temperature_trend": temperature,

            "humidity_trend": humidity,

            "rainfall_trend": rainfall,

            "wind_speed_trend": wind

        }

    # ==========================================================
    # Crop Stress Index
    # ==========================================================

    def calculate_crop_stress(
        self,
        analytics: Dict[str, Any]
    ):

        stress = []

        for temp, humidity in zip(
            analytics["temperature_trend"],
            analytics["humidity_trend"]
        ):

            score = 0

            if temp >= 40:
                score += 50

            elif temp >= 35:
                score += 35

            elif temp >= 30:
                score += 20

            if humidity < 35:
                score += 40

            elif humidity < 50:
                score += 20

            stress.append(min(score, 100))

        analytics["crop_stress_index"] = stress

        return analytics

    # ==========================================================
    # Irrigation Index
    # ==========================================================

    def calculate_irrigation_index(
        self,
        analytics: Dict[str, Any]
    ):

        irrigation = []

        for rain, temp in zip(
            analytics["rainfall_trend"],
            analytics["temperature_trend"]
        ):

            score = 100

            score -= rain * 5

            if temp < 22:
                score -= 10

            score = max(0, min(int(score), 100))

            irrigation.append(score)

        analytics["irrigation_index"] = irrigation

        return analytics