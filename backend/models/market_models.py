from pydantic import BaseModel


class MarketRequest(BaseModel):

    crop: str

    state: str

    district: str


class MarketResponse(BaseModel):

    crop: str

    market: str

    district: str

    state: str

    current_price: float

    average_price: float

    minimum_price: float

    maximum_price: float

    arrival_quantity: float

    unit: str

    market_trend: str

    price_forecast: str

    profit_potential: str

    confidence: int