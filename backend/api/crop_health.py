import io
from PIL import Image

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

from agents.crop_health_agent import CropHealthAgent
from models.crop_health_models import CropHealthResponse

router = APIRouter(
    prefix="/crop-health",
    tags=["Crop Health"]
)

agent = CropHealthAgent()


@router.post(
    "/analyze",
    response_model=CropHealthResponse
)
async def analyze_crop(
    crop: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # Read uploaded image bytes and convert to a PIL Image object
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Pass parameters matching CropHealthAgent signature
        result = agent.analyze_crop(
            crop=crop,
            image=pil_image
        )

        # Ensure missing fields expected by CropHealthResponse model are populated
        result.setdefault("history", [])
        result.setdefault("comparison", {})
        result.setdefault("graph_data", [])

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )