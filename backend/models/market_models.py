from typing import Any, Dict
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
    arrival_quantity: int
    unit: str
    market_trend: str
    price_forecast: str
    profit_potential: str
    confidence: int


class AnalyzeCropRequest(BaseModel):
    crop: str


class AnalyzeCropResponse(BaseModel):
    crop: str
    market: str
    district: str
    state: str
    current_price: float
    average_price: float
    minimum_price: float
    maximum_price: float
    arrival_quantity: int
    unit: str
    market_trend: str
    price_forecast: str
    profit_potential: str
    confidence: int
    price_history: list[float]
    price_prediction: list[float]
    reasoning: str


class CompareCropRequest(BaseModel):
    crop1: str
    crop2: str


class CompareCropResponse(BaseModel):
    crop1: AnalyzeCropResponse
    crop2: AnalyzeCropResponse
    recommended_crop: str
    comparison_reasoning: str