from fastapi import APIRouter, HTTPException

from agents.climate_intelligence_agent import ClimateAgent
from agents.crop_planning_agent import CropPlanningAgent

from models.crop_plan import CropPlanningRequest, CropPlanningResponse

router = APIRouter(
    prefix="/crop",
    tags=["Crop Planning"]
)

climate_agent = ClimateAgent()
crop_agent = CropPlanningAgent()


@router.post(
    "/recommend",
    response_model=CropPlanningResponse
)
def recommend(request: CropPlanningRequest):

    try:
        climate = climate_agent.analyze(request.city)

        climate_data = {
            "temperature": climate["temperature"],
            "humidity": climate["humidity"],
            "rainfall": climate["rainfall"]
        }

        recommendations = crop_agent.recommend_crops(
            climate_data=climate_data,
            soil_ph=request.soil_ph,
            state=getattr(request, "state", None),
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