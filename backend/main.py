"""
🌾 Smart Agriculture Intelligence System
Main FastAPI Application — Entry Point

Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models.yield_model import load_model, get_model_metrics
from routes import prediction, simulation, risk_alerts, heatmap, soil, disease, schemes, communication, offline, auth
import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize ML model on startup."""
    print("\n" + "=" * 60)
    print(" Smart Agriculture Intelligence System")
    print("=" * 60)
    load_model()
    metrics = get_model_metrics()
    if metrics:
        print(f"📊 Model R² Score: {metrics.get('r2_score', 'N/A')}")
        print(f"📊 Model MAE: {metrics.get('mae', 'N/A')}")
    print("✅ System ready!")
    print("=" * 60 + "\n")
    yield
    print("\n🛑 Shutting down...")


app = FastAPI(
    title="🌾 Smart Agriculture Intelligence System",
    description=(
        "ML-powered Crop Yield Prediction Engine with What-If Simulator, "
        "Risk Alerts, Zone Heatmaps, Soil Analysis, Disease Detection, "
        "Government Schemes, and SMS/WhatsApp Integration.\n\n"
        "**Core Module:** Crop Yield Prediction using RandomForest ML Model\n"
        "**Target Region:** Karnataka, India"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routes ────────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(risk_alerts.router, prefix="/api")
app.include_router(heatmap.router, prefix="/api")
app.include_router(soil.router, prefix="/api")
app.include_router(disease.router, prefix="/api")
app.include_router(schemes.router, prefix="/api")
app.include_router(communication.router, prefix="/api")
app.include_router(offline.router, prefix="/api")


@app.get("/", tags=["🏠 Home"])
async def root():
    return {
        "system": "Smart Agriculture Intelligence System",
        "version": "1.0.0",
        "status": "running",
        "core_module": "Crop Yield Prediction Engine (RandomForest ML)",
        "endpoints": {
            "login": "POST /api/login",
            "predict_yield": "POST /api/predict-yield",
            "simulate_yield": "POST /api/simulate-yield",
            "risk_alerts": "POST /api/risk-alerts",
            "yield_heatmap": "GET /api/yield-heatmap",
            "soil_analysis": "POST /api/soil-analysis",
            "disease_detection": "POST /api/disease-detection",
            "government_schemes": "GET /api/schemes",
            "check_eligibility": "POST /api/check-eligibility",
            "send_sms": "POST /api/send-sms",
            "chat": "POST /api/chat",
            "offline_query": "POST /api/offline-query",
            "sms_webhook": "POST /api/webhook/sms",
        },
        "docs": "/docs",
    }


@app.get("/health", tags=["🏠 Home"])
async def health_check():
    metrics = get_model_metrics()
    return {
        "status": "healthy",
        "model_loaded": metrics is not None and len(metrics) > 0,
        "model_metrics": metrics,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
