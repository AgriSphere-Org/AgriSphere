from pydantic import BaseModel
from typing import Dict, Any


class WeatherResponse(BaseModel):

    location: str

    temperature: float

    humidity: float

    rainfall: float

    wind_speed: float

    heat_stress: str

    drought_risk: str

    flood_risk: str

    farming_condition: str

    recommendation: str

    forecast: Dict[str, Any]