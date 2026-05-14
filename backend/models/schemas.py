"""
Pydantic schemas for request/response validation across all endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ─── Enums ───────────────────────────────────────────────────────

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    KANNADA = "kn"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class YieldCategory(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    AVERAGE = "average"
    GOOD = "good"
    EXCELLENT = "excellent"


class ZoneLabel(str, Enum):
    HIGH = "High Yield"
    MEDIUM = "Medium Yield"
    LOW = "Low Yield"


# ─── Yield Prediction ───────────────────────────────────────────

class YieldPredictionRequest(BaseModel):
    rainfall_mm: float = Field(..., ge=0, le=3000, description="Rainfall in millimeters")
    temperature_c: float = Field(..., ge=-10, le=55, description="Temperature in Celsius")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    soil_moisture_pct: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    fertilizer_kg_per_hectare: float = Field(..., ge=0, le=500, description="Fertilizer usage in kg/hectare")
    irrigation_level_pct: float = Field(..., ge=0, le=100, description="Irrigation level percentage")
    language: Language = Field(default=Language.ENGLISH, description="Output language")

    class Config:
        json_schema_extra = {
            "example": {
                "rainfall_mm": 750,
                "temperature_c": 28,
                "soil_ph": 6.5,
                "soil_moisture_pct": 45,
                "fertilizer_kg_per_hectare": 80,
                "irrigation_level_pct": 60,
                "language": "en",
            }
        }


class YieldPredictionResponse(BaseModel):
    predicted_yield_tons_per_hectare: float
    yield_category: YieldCategory
    interpretation: str
    confidence_score: float
    recommendations: List[str]


# ─── Simulation ──────────────────────────────────────────────────

class SimulationRequest(BaseModel):
    # Original conditions
    original: YieldPredictionRequest

    # Modified conditions for simulation
    simulated_rainfall_mm: Optional[float] = Field(None, ge=0, le=3000)
    simulated_temperature_c: Optional[float] = Field(None, ge=-10, le=55)
    simulated_soil_ph: Optional[float] = Field(None, ge=0, le=14)
    simulated_soil_moisture_pct: Optional[float] = Field(None, ge=0, le=100)
    simulated_fertilizer_kg_per_hectare: Optional[float] = Field(None, ge=0, le=500)
    simulated_irrigation_level_pct: Optional[float] = Field(None, ge=0, le=100)
    language: Language = Field(default=Language.ENGLISH)

    class Config:
        json_schema_extra = {
            "example": {
                "original": {
                    "rainfall_mm": 750,
                    "temperature_c": 28,
                    "soil_ph": 6.5,
                    "soil_moisture_pct": 45,
                    "fertilizer_kg_per_hectare": 80,
                    "irrigation_level_pct": 60,
                },
                "simulated_irrigation_level_pct": 85,
                "simulated_fertilizer_kg_per_hectare": 120,
                "language": "en",
            }
        }


class SimulationResponse(BaseModel):
    original_yield: float
    simulated_yield: float
    yield_change_tons: float
    yield_change_pct: float
    original_interpretation: str
    simulated_interpretation: str
    comparison_summary: str
    modifications_applied: dict


# ─── Risk Alerts ─────────────────────────────────────────────────

class RiskAlertRequest(BaseModel):
    rainfall_mm: float = Field(..., ge=0, le=3000)
    temperature_c: float = Field(..., ge=-10, le=55)
    soil_ph: float = Field(..., ge=0, le=14)
    soil_moisture_pct: float = Field(..., ge=0, le=100)
    fertilizer_kg_per_hectare: float = Field(..., ge=0, le=500)
    irrigation_level_pct: float = Field(..., ge=0, le=100)
    language: Language = Field(default=Language.ENGLISH)


class RiskAlert(BaseModel):
    risk_type: str
    risk_level: RiskLevel
    message: str
    recommendation: str
    icon: str


class RiskAlertResponse(BaseModel):
    total_alerts: int
    overall_risk_level: RiskLevel
    alerts: List[RiskAlert]
    summary: str


# ─── Heatmap ─────────────────────────────────────────────────────

class ZoneYieldData(BaseModel):
    zone_id: str
    zone_name: str
    latitude: float
    longitude: float
    predicted_yield: float
    yield_label: ZoneLabel
    color_code: str


class HeatmapResponse(BaseModel):
    total_zones: int
    zones: List[ZoneYieldData]
    generated_at: str
    summary: dict


# ─── Soil Analysis ───────────────────────────────────────────────

class SoilAnalysisRequest(BaseModel):
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    soil_moisture_pct: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    language: Language = Field(default=Language.ENGLISH)


class SoilAnalysisResponse(BaseModel):
    soil_quality: str
    ph_status: str
    moisture_status: str
    recommendations: List[str]
    suitable_crops: List[str]


# ─── Disease Detection ──────────────────────────────────────────

class DiseaseDetectionResponse(BaseModel):
    disease_detected: bool
    disease_name: str
    confidence: float
    description: str
    suggestions: List[str]


# ─── Government Schemes ─────────────────────────────────────────

class SchemeEligibilityRequest(BaseModel):
    is_farmer: bool = True
    age: int = Field(..., ge=0, le=120)
    land_holding_hectares: float = Field(..., ge=0)
    state: str = "Karnataka"
    has_crop: bool = True
    language: Language = Field(default=Language.ENGLISH)


class SchemeInfo(BaseModel):
    id: str
    name: str
    full_name: str
    description: str
    benefit: str
    eligible: bool
    reason: str
    documents_required: List[str]
    website: str


class SchemeResponse(BaseModel):
    total_schemes: int
    eligible_count: int
    schemes: List[SchemeInfo]


# ─── SMS / Communication ────────────────────────────────────────

class SMSRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 format")
    message: str = Field(..., description="Message content")


class SMSResponse(BaseModel):
    success: bool
    message_sid: str
    status: str
    detail: str


class ChatQueryRequest(BaseModel):
    query: str = Field(..., description="Farmer's question in natural language")
    language: Language = Field(default=Language.ENGLISH)


class ChatQueryResponse(BaseModel):
    query: str
    response: str
    detected_intent: str
    suggestions: List[str]


# ─── Offline SMS Commands ───────────────────────────────────────

class OfflineSMSRequest(BaseModel):
    sms_body: str = Field(..., description="Raw SMS text like 'YIELD 750 28 6.5 45 80 60'")
    sender_phone: str = Field(default="+910000000000")


class OfflineSMSResponse(BaseModel):
    parsed_successfully: bool
    command: str
    prediction_result: Optional[dict] = None
    reply_message: str
    error: Optional[str] = None


# ─── Authentication ──────────────────────────────────────────────

class FarmerLoginRequest(BaseModel):
    aadhaar_number: str = Field(..., min_length=12, max_length=12, description="12-digit Aadhaar Number")
    phone_number: str = Field(..., description="Phone number to send login SMS to (E.164 format)")

class FarmerLoginResponse(BaseModel):
    success: bool
    message: str
    session_token: Optional[str] = None
    sms_status: str

# ─── Internal & History Schemas ──────────────────────────────────

class CurrentFarmer(BaseModel):
    aadhaar_number: str
    phone_number: str

class PredictionHistoryItem(BaseModel):
    id: str = Field(alias="_id", default="")
    farmer_aadhaar: str
    timestamp: str
    input_params: dict
    predicted_yield: float
    yield_rating: str
    recommendations: List[str]
    language: str

class PredictionHistoryResponse(BaseModel):
    total: int
    predictions: List[PredictionHistoryItem]

class AlertHistoryItem(BaseModel):
    id: str = Field(alias="_id", default="")
    farmer_aadhaar: str
    timestamp: str
    alerts_generated: List[dict]

class AlertHistoryResponse(BaseModel):
    total: int
    alerts: List[AlertHistoryItem]


# ─── Voice AI Assistant ──────────────────────────────────────────

class VoiceAssistantResponse(BaseModel):
    transcription: str
    text_response: str
    audio_url: str
    detected_intent: str


# ─── Knowledge Garden ────────────────────────────────────────────

class MultilingualText(BaseModel):
    en: str
    hi: str
    kn: str

class FarmingTerm(BaseModel):
    id: str
    name: MultilingualText
    definition: MultilingualText
    category: str

class KnowledgeGardenResponse(BaseModel):
    total: int
    terms: List[FarmingTerm]

