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

        # ------------------------------------------
        # Validate input
        # ------------------------------------------

        if not request.crop or not request.crop.strip():

            raise HTTPException(
                status_code=400,
                detail="Crop name is required."
            )

        if not request.state or not request.state.strip():

            raise HTTPException(
                status_code=400,
                detail="State is required."
            )

        if (
            not request.district
            or not request.district.strip()
        ):

            raise HTTPException(
                status_code=400,
                detail="District is required."
            )

        # ------------------------------------------
        # Market Intelligence Agent
        # ------------------------------------------

        result = agent.analyze_market(

            crop=request.crop.strip(),

            state=request.state.strip(),

            district=request.district.strip()

        )

        # ------------------------------------------
        # No data
        # ------------------------------------------

        if not result:

            raise HTTPException(

                status_code=404,

                detail=(
                    "No market data found for "
                    f"{request.crop}, "
                    f"{request.district}, "
                    f"{request.state}."
                )

            )

        return result

    # ----------------------------------------------
    # Preserve FastAPI HTTP errors
    # ----------------------------------------------

    except HTTPException:

        raise

    # ----------------------------------------------
    # Other errors
    # ----------------------------------------------

    except ValueError as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Market analysis failed: {str(e)}"

        )