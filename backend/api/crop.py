from fastapi import APIRouter, HTTPException

from services.weather_service import WeatherService
from agents.crop_planning_agent import CropPlanningAgent

from models.crop_plan import CropPlanningRequest, CropPlanningResponse

router = APIRouter(
    prefix="/crop",
    tags=["Crop Planning"]
)

weather_service = WeatherService()
crop_agent = CropPlanningAgent()


@router.post(
    "/recommend",
    response_model=CropPlanningResponse
)
def recommend(request: CropPlanningRequest):

    try:
        # ------------------------------------------
        # Get weather data using city/district
        # ------------------------------------------

        weather = weather_service.get_current_weather(
            request.state,
            request.city
        )

        # ------------------------------------------
        # Extract climate data
        # ------------------------------------------

        main = weather.get("main", {})
        rain = weather.get("rain", {})

        climate_data = {
            "temperature": main.get("temp", 0),
            "humidity": main.get("humidity", 0),
            "rainfall": rain.get(
                "1h",
                rain.get("3h", 0)
            )
        }

        # ------------------------------------------
        # Crop recommendations
        # ------------------------------------------

        recommendations = crop_agent.recommend_crops(
            climate_data=climate_data,
            soil_ph=request.soil_ph,
            state=request.state,
            top_n=10
        )

        return {
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )