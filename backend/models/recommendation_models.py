from typing import List
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):

    crop: str = Field(
        ...,
        description="Name of the crop",
        examples=["Rice"]
    )

    state: str = Field(
        ...,
        description="State where the farm is located",
        examples=["Maharashtra"]
    )

    soil_ph: float = Field(
        ...,
        ge=0,
        le=14,
        description="Soil pH value",
        examples=[6.0]
    )


class RecommendationItem(BaseModel):

    priority: int = Field(
        ...,
        description="Priority of the recommendation"
    )

    area: str = Field(
        ...,
        description="Agricultural area such as Soil, Nutrients, Water, or Crop Protection"
    )

    recommendation: str = Field(
        ...,
        description="Short and practical recommendation for the farmer"
    )


class RecommendationResponse(BaseModel):

    crop: str

    state: str

    soil_ph: float

    recommendations: List[RecommendationItem]

    overall_advice: str = Field(
        ...,
        description="Short overall agricultural advice"
    )