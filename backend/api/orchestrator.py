from typing import Optional
import os

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from agents.orchestrator import AgriSphereOrchestrator


router = APIRouter(
    prefix="/orchestrator",
    tags=["Orchestrator"],
)


orchestrator = AgriSphereOrchestrator()


@router.post("/analyze")
async def analyze_farm(

    city: str = Form(...),

    soil_ph: float = Form(...),

    state: str = Form(...),

    district: str = Form(...),

    farmer_category: str = Form(...),

    farm_size: float = Form(...),

    irrigation: str = Form(...),

    gender: str = Form(...),

    age: int = Form(...),

    question: Optional[str] = Form(None),

    crop_image: UploadFile = File(...),

):

    image_path = None

    try:

        # ======================================================
        # SAVE TEMPORARY CROP IMAGE
        # ======================================================

        image_path = f"temp_{crop_image.filename}"

        with open(image_path, "wb") as file:

            file.write(
                await crop_image.read()
            )

        # ======================================================
        # RUN AGRISPHERE ORCHESTRATOR
        # ======================================================

        result = orchestrator.run(

            city=city,

            soil_ph=soil_ph,

            crop_image_path=image_path,

            state=state,

            district=district,

            farmer_category=farmer_category,

            farm_size=farm_size,

            irrigation=irrigation,

            gender=gender,

            age=age,

            question=question,

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

    finally:

        # ======================================================
        # DELETE TEMPORARY IMAGE
        # ======================================================

        if image_path and os.path.exists(image_path):

            os.remove(image_path)