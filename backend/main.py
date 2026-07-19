from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.weather import router as weather_router
from api.crop import router as crop_router
from api.crop_health import router as crop_health_router
from api.market import router as market_router
from api.government_scheme import router as government_router
from api.knowledge import router as knowledge_router
from api.orchestrator import router as orchestrator_router

app = FastAPI(
    title="AgriSphere AI",
    description="A Multi-Agent Climate & Agriculture Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # React (Vite)
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register API Routers
# -----------------------------

app.include_router(weather_router)

app.include_router(crop_router)

app.include_router(crop_health_router)

app.include_router(market_router)

app.include_router(government_router)

app.include_router(knowledge_router)

app.include_router(orchestrator_router)

# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/", tags=["Home"])
def home():

    return {
        "application": "AgriSphere AI",
        "version": "1.0.0",
        "status": "Running",
        "message": "Welcome to AgriSphere AI 🌾",
        "documentation": "/docs"
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health", tags=["Health"])
def health():

    return {
        "status": "healthy",
        "service": "AgriSphere AI",
        "version": "1.0.0"
    }


# -----------------------------
# API Information
# -----------------------------

@app.get("/info", tags=["Information"])
def info():

    return {
        "Project": "AgriSphere AI",
        "Architecture": "Multi-Agent AI",
        "Backend": "FastAPI",
        "Frontend": "React + Vite",
        "Database": "PostgreSQL",
        "AI": "Google Gemini",
        "Modules": [
            "Climate Intelligence",
            "Crop Planning",
            "Crop Health Detection",
            "Market Intelligence",
            "Government Scheme Recommendation",
            "Knowledge (RAG)",
            "Recommendation Engine",
            "Orchestrator"
        ]
    }