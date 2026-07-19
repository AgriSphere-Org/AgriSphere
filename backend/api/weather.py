from fastapi import APIRouter, HTTPException
from agents.climate_intelligence_agent import ClimateAgent
from models.weather_log import WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["Climate Intelligence"]
)

agent = ClimateAgent()


@router.get(
    "/{city}",
    response_model=WeatherResponse
)
def weather(city: str):

    try:

        return agent.analyze(city)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )