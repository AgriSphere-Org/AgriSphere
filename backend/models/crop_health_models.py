from typing import Any, Dict, List
from pydantic import BaseModel


class CropHealthResponse(BaseModel):

    crop: str

    disease: str

    confidence: float

    health_score: int

    severity: str

    recommendation: str

    status: str

    history: List[Dict[str, Any]]

    comparison: Dict[str, Any]

    graph_data: List[int]