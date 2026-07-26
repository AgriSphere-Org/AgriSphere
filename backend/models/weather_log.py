from pydantic import BaseModel
from typing import List, Optional


# ==========================================================
# Request Model
# ==========================================================

class WeatherRequest(BaseModel):
    state: str
    district: str
    village: Optional[str] = None
    crop: str


# ==========================================================
# Current Weather
# ==========================================================

class CurrentWeather(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float
    weather: str


# ==========================================================
# Climate Advisory
# ==========================================================

class ClimateAdvisory(BaseModel):
    farming_condition: str

    recommendation: str

    irrigation_advice: str

    disease_risk: str

    heat_stress: str

    drought_risk: str

    flood_risk: str


# ==========================================================
# Weather Analytics (Graph Data)
# ==========================================================

class WeatherAnalytics(BaseModel):
    dates: List[str]

    temperature_trend: List[float]

    humidity_trend: List[float]

    rainfall_trend: List[float]

    wind_speed_trend: List[float]

    crop_stress_index: List[int]

    irrigation_index: List[int]


# ==========================================================
# Response Model
# ==========================================================

class WeatherResponse(BaseModel):
    location: str

    crop: str

    current_weather: CurrentWeather

    advisory: ClimateAdvisory

    analytics: WeatherAnalytics