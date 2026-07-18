from fastapi import APIRouter, HTTPException

from agents.climate_intelligence_agent import ClimateAgent
from agents.crop_planning_agent import CropPlanningAgent

from models.crop_plan import *

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

        recommendations = crop_agent.recommend_crop(

            temperature=climate["temperature"],

            humidity=climate["humidity"],

            rainfall=climate["rainfall"],

            soil_ph=request.soil_ph

        )

        return {

            "recommendations": recommendations

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )