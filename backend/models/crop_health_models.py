from typing import List, Optional
from pydantic import BaseModel, Field


class CropHealthResponse(BaseModel):

    # Crop information
    crop: str
    detected_crop: Optional[str] = None
    crop_match: Optional[bool] = None

    # Image quality
    image_quality: str

    # Health analysis
    health_status: str
    disease: Optional[str] = None
    health_score: int
    severity: str

    # AI reasoning
    visible_symptoms: List[str] = Field(default_factory=list)
    analysis_summary: str