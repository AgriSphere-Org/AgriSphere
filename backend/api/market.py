from fastapi import APIRouter, HTTPException

from agents.market_agent import MarketAgent
from models.market_models import (
    AnalyzeCropRequest,
    AnalyzeCropResponse,
    CompareCropRequest,
    CompareCropResponse,
    MarketRequest,
    MarketResponse,
)

router = APIRouter(prefix="/market", tags=["Market Intelligence"])
agent = MarketAgent()


@router.post(
    "/analyze",
    response_model=MarketResponse,
    summary="Analyze specific market prices",
    description="Analyzes market intelligence data, price trends, forecasts, and profit potential for a specific crop, state, and district.",
)
async def analyze_market(request: MarketRequest):
    try:
        return agent.analyze_market(
            crop=request.crop, state=request.state, district=request.district
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/crop-analysis",
    response_model=AnalyzeCropResponse,
    summary="Comprehensive single-crop analysis",
    description="Provides detailed market analytics for a single crop, including historical price trends, future price predictions, and automated reasoning.",
)
async def analyze_crop(request: AnalyzeCropRequest):
    try:
        return agent.analyze_crop(crop=request.crop)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/compare",
    response_model=CompareCropResponse,
    summary="Compare market trends between two crops",
    description="Compares market trends, profitability potential, and confidence scores between two crops to provide a recommended crop choice and comparative reasoning.",
)
async def compare_crops(request: CompareCropRequest):
    try:
        return agent.compare_crop_trends(crop1=request.crop1, crop2=request.crop2)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))