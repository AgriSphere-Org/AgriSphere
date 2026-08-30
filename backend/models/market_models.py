from typing import Optional

from pydantic import BaseModel, Field


# =========================================================
# MARKET REQUEST
# =========================================================

class MarketRequest(BaseModel):

    crop: str = Field(
        ...,
        min_length=1,
        description="Crop name, e.g. Wheat"
    )

    state: str = Field(
        ...,
        min_length=1,
        description="Indian state, e.g. Punjab"
    )

    district: str = Field(
        ...,
        min_length=1,
        description="District name, e.g. Amritsar"
    )


# =========================================================
# MARKET RESPONSE
# =========================================================

class MarketResponse(BaseModel):

    # -----------------------------------------------------
    # Location / Commodity
    # -----------------------------------------------------

    crop: str

    market: str

    district: str

    state: str


    # -----------------------------------------------------
    # Current Mandi Prices
    # -----------------------------------------------------

    current_price: float

    average_price: float

    minimum_price: float

    maximum_price: float


    # -----------------------------------------------------
    # Market Arrivals
    # -----------------------------------------------------

    arrival_quantity: float

    unit: str


    # -----------------------------------------------------
    # AI Market Analysis
    # -----------------------------------------------------

    market_trend: str

    price_forecast: str

    profit_potential: str

    confidence: int


    # -----------------------------------------------------
    # Live API Metadata
    # -----------------------------------------------------

    last_updated: Optional[str] = None

    data_source: Optional[str] = (
        "Government of India - data.gov.in / Agmarknet"
    )