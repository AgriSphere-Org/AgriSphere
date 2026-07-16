from fastapi import FastAPI

from api.crop_health import router as crop_health_router
from api.knowledge import router as knowledge_router
from api.market import router as market_router
from api.recommendation import router as recommendation_router

app = FastAPI(
    title="AgriSphere AI",
    version="1.0.0"
)

app.include_router(crop_health_router)
app.include_router(knowledge_router)
app.include_router(market_router)
app.include_router(recommendation_router)


@app.get("/")
def home():
    return {
        "message": "AgriSphere Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }