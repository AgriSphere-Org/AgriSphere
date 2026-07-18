from fastapi import APIRouter, HTTPException

from agents.market_agent import MarketAgent

from models.market_models import (

    MarketRequest,

    MarketResponse

)

router = APIRouter(

    prefix="/market",

    tags=["Market Intelligence"]

)

agent = MarketAgent()


@router.post(

    "/analyze",

    response_model=MarketResponse

)

def analyze_market(

    request: MarketRequest

):

    try:

        result = agent.analyze_market(

            crop=request.crop,

            state=request.state,

            district=request.district

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )