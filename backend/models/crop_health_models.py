from pydantic import BaseModel


class CropHealthResponse(BaseModel):

    crop: str

    disease: str

    confidence: float

    health_score: int

    severity: str

    recommendation: str