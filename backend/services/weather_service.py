import requests
import logging
from typing import Dict, Any

from config.settings import WEATHER_API_KEY

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Handles communication with the external weather API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        if not WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is missing from environment variables.")

        self.api_key = WEATHER_API_KEY

    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """
        Fetch current weather for a city.
        """

        endpoint = f"{self.BASE_URL}/weather"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            logger.info(f"Current weather fetched for {city}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Current weather API error: {e}")
            raise RuntimeError("Unable to fetch current weather.")

    def get_forecast(self, city: str) -> Dict[str, Any]:
        """
        Fetch 5-day weather forecast.
        """

        endpoint = f"{self.BASE_URL}/forecast"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            logger.info(f"Forecast fetched for {city}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Forecast API error: {e}")
            raise RuntimeError("Unable to fetch weather forecast.")