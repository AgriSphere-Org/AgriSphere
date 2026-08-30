import os
import shutil
import uuid
from typing import Optional

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

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post(
    "/analyze",
    response_model=CropHealthResponse
)
async def analyze_crop(
    crop: Optional[str] = Form(None),
    image: UploadFile = File(...)
):

    image_path = None

    try:

        # -------------------------------
        # Validate file extension
        # -------------------------------

        if not image.filename:
            raise HTTPException(
                status_code=400,
                detail="No image selected."
            )

        extension = image.filename.split(".")[-1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        # -------------------------------
        # Validate file size
        # -------------------------------

        image_bytes = await image.read()

        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Image size exceeds 10 MB."
            )

        # Reset pointer
        image.file.seek(0)

        # -------------------------------
        # Save image temporarily
        # -------------------------------

        filename = f"{uuid.uuid4()}.{extension}"

        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )

        # -------------------------------
        # Analyze Crop
        # -------------------------------

        result = agent.analyze_crop(
            crop=crop,
            image_path=image_path
        )

        return result

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Crop analysis failed: {str(e)}"
        )

    finally:

        if image_path and os.path.exists(image_path):
            os.remove(image_path)