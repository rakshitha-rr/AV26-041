"""
Configuration module for the Smart Agriculture Intelligence System.
Loads environment variables and defines system-wide constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── Server Config ───────────────────────────────────────────────
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# ─── Database Config ─────────────────────────────────────────────
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "agriintel")

# ─── Twilio Config ───────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

# ─── ML Model Config ────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_models", "yield_model.joblib")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "data", "karnataka_crop_data.csv")
TRAINING_SAMPLES = 5000

# ─── Yield Thresholds (tons/hectare) ────────────────────────────
YIELD_THRESHOLDS = {
    "very_low": 1.5,
    "low": 2.5,
    "average": 3.5,
    "good": 4.5,
    "excellent": 5.5,
}

# ─── Risk Thresholds ────────────────────────────────────────────
RISK_THRESHOLDS = {
    "drought": {
        "rainfall_below": 300,
        "temperature_above": 35,
    },
    "crop_stress": {
        "ph_low": 5.0,
        "ph_high": 8.5,
        "moisture_below": 20,
        "temperature_above": 38,
    },
    "disease": {
        "moisture_above": 65,
        "temperature_range": (22, 32),
        "humidity_factor": 0.7,
    },
}

# ─── Karnataka Zones ────────────────────────────────────────────
KARNATAKA_ZONES = [
    {"zone_id": "KA-01", "name": "Bengaluru Rural", "lat": 13.0, "lng": 77.5},
    {"zone_id": "KA-02", "name": "Mysuru", "lat": 12.3, "lng": 76.6},
    {"zone_id": "KA-03", "name": "Mandya", "lat": 12.5, "lng": 76.9},
    {"zone_id": "KA-04", "name": "Hassan", "lat": 13.0, "lng": 76.1},
    {"zone_id": "KA-05", "name": "Tumkur", "lat": 13.3, "lng": 77.1},
    {"zone_id": "KA-06", "name": "Chitradurga", "lat": 14.2, "lng": 76.4},
    {"zone_id": "KA-07", "name": "Davangere", "lat": 14.5, "lng": 75.9},
    {"zone_id": "KA-08", "name": "Shimoga", "lat": 13.9, "lng": 75.6},
    {"zone_id": "KA-09", "name": "Dharwad", "lat": 15.5, "lng": 75.0},
    {"zone_id": "KA-10", "name": "Belagavi", "lat": 15.8, "lng": 74.5},
    {"zone_id": "KA-11", "name": "Raichur", "lat": 16.2, "lng": 77.4},
    {"zone_id": "KA-12", "name": "Ballari", "lat": 15.1, "lng": 76.9},
    {"zone_id": "KA-13", "name": "Kalaburagi", "lat": 17.3, "lng": 76.8},
    {"zone_id": "KA-14", "name": "Bidar", "lat": 17.9, "lng": 77.5},
    {"zone_id": "KA-15", "name": "Kodagu", "lat": 12.4, "lng": 75.7},
    {"zone_id": "KA-16", "name": "Udupi", "lat": 13.3, "lng": 74.7},
    {"zone_id": "KA-17", "name": "Dakshina Kannada", "lat": 12.9, "lng": 74.9},
    {"zone_id": "KA-18", "name": "Haveri", "lat": 14.8, "lng": 75.4},
    {"zone_id": "KA-19", "name": "Gadag", "lat": 15.4, "lng": 75.6},
    {"zone_id": "KA-20", "name": "Koppal", "lat": 15.3, "lng": 76.2},
]

# ─── Government Schemes ─────────────────────────────────────────
GOVERNMENT_SCHEMES = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "description": "Income support of ₹6,000/year to small and marginal farmer families with cultivable land holding up to 2 hectares.",
        "benefit": "₹6,000 per year in 3 installments",
        "eligibility": {
            "land_holding_max_hectares": 2.0,
            "must_be_farmer": True,
            "min_age": 18,
        },
        "documents_required": ["Aadhaar Card", "Land Records", "Bank Account"],
        "website": "https://pmkisan.gov.in",
    },
    {
        "id": "soil-health-card",
        "name": "Soil Health Card Scheme",
        "full_name": "Soil Health Card Scheme",
        "description": "Provides soil health cards to farmers carrying crop-wise recommendations on nutrients and fertilizers.",
        "benefit": "Free soil testing and nutrient recommendations",
        "eligibility": {
            "must_be_farmer": True,
            "min_age": 18,
        },
        "documents_required": ["Aadhaar Card", "Land Records"],
        "website": "https://soilhealth.dac.gov.in",
    },
    {
        "id": "pmfby",
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "description": "Crop insurance scheme covering yield losses due to natural calamities, pests, and diseases.",
        "benefit": "Insurance coverage at low premium: 2% for Kharif, 1.5% for Rabi",
        "eligibility": {
            "must_be_farmer": True,
            "min_age": 18,
            "must_have_crop": True,
        },
        "documents_required": ["Aadhaar Card", "Land Records", "Bank Account", "Sowing Certificate"],
        "website": "https://pmfby.gov.in",
    },
    {
        "id": "krishi-sinchai",
        "name": "PMKSY",
        "full_name": "Pradhan Mantri Krishi Sinchai Yojana",
        "description": "Ensures access to protective irrigation for every farm (Har Khet Ko Paani) and improves water use efficiency.",
        "benefit": "Subsidy for micro-irrigation systems (drip/sprinkler)",
        "eligibility": {
            "must_be_farmer": True,
            "min_age": 18,
        },
        "documents_required": ["Aadhaar Card", "Land Records", "Bank Account"],
        "website": "https://pmksy.gov.in",
    },
    {
        "id": "raitha-siri",
        "name": "Raitha Siri",
        "full_name": "Karnataka Raitha Siri Scheme",
        "description": "Karnataka state scheme providing financial assistance for crop production and farm mechanization.",
        "benefit": "Subsidies on farm equipment and inputs",
        "eligibility": {
            "must_be_farmer": True,
            "min_age": 18,
            "state": "Karnataka",
        },
        "documents_required": ["Aadhaar Card", "Land Records", "Caste Certificate (if applicable)"],
        "website": "https://raitamitra.karnataka.gov.in",
    },
]
