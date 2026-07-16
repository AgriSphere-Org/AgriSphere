import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
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


@router.post(

    "/analyze",

    response_model=CropHealthResponse

)

async def analyze_crop(

    image: UploadFile = File(...)

):

    try:

        extension = image.filename.split(".")[-1]

        filename = f"{uuid.uuid4()}.{extension}"

        image_path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        with open(

            image_path,

            "wb"

        ) as buffer:

            shutil.copyfileobj(

                image.file,

                buffer

            )

        result = agent.analyze_crop(

            image_path

        )

        os.remove(image_path)

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )