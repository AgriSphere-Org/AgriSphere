from fastapi import FastAPI

from api.weather import router as weather_router
from api.crop import router as crop_router
from api.government_scheme import router as government_router

app = FastAPI(

    title="AgriSphere AI",

    version="1.0.0"

)

app.include_router(weather_router)

app.include_router(crop_router)

app.include_router(government_router)


@app.get("/")
def home():

    return {

        "message": "Welcome to AgriSphere AI 🌾"

    }


@app.get("/health")
def health():

    return {

        "status": "running",

        "service": "AgriSphere AI"

    }