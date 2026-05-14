# AgriIntel: Smart Agriculture Intelligence System Backend

A robust, production-ready FastAPI backend designed to empower farmers in Karnataka with ML-driven insights, risk alerts, and data-backed agricultural recommendations.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file for Twilio SMS integration:
   ```env
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number
   ```

### Running the Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
The server will start at `http://localhost:8000`. You can view the interactive Swagger UI documentation at `http://localhost:8000/docs`.

---

## 📂 Project Structure

```text
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # System-wide configuration and constants
├── data/
│   └── generate_dataset.py # Synthetic data generator for the ML model
├── models/
│   ├── schemas.py          # Pydantic models for API request/response validation
│   ├── yield_model.py      # RandomForest ML model for crop yield prediction
│   └── risk_model.py       # Rule-based engine for detecting agricultural risks
├── routes/
│   ├── auth.py             # Farmer Aadhaar Login endpoint
│   ├── prediction.py       # Core Yield Prediction endpoint
│   ├── simulation.py       # What-If Simulator endpoint
│   ├── risk_alerts.py      # Drought, stress, disease risk alerts
│   ├── heatmap.py          # Zone-wise yield generation
│   ├── soil.py             # Soil analysis endpoint
│   ├── disease.py          # Crop disease detection endpoint
│   ├── schemes.py          # Gov schemes and eligibility endpoints
│   ├── communication.py    # NLP chat and SMS sender
│   └── offline.py          # Offline SMS command parser
└── utils/
    ├── interpreter.py      # Converts ML numerical outputs into farmer-friendly text
    ├── translator.py       # Multilingual support (EN, HI, KN)
    └── sms_handler.py      # Twilio integration and NLP logic
```

---

## 📡 API Reference

All endpoints are prefixed with `/api`.

### 1. Authentication
**`POST /api/login`**
Farmer login using an Aadhaar number. Triggers a welcome SMS on success.
- **Request Body**:
  ```json
  {
    "aadhaar_number": "123456789012",
    "phone_number": "+919876543210"
  }
  ```
- **Response**: `{ "success": true, "message": "Login successful", "sms_status": "queued" }`

### 2. Core Yield Prediction
**`POST /api/predict-yield`**
Predicts the crop yield (tons/hectare) using the RandomForest model based on climate and soil parameters.
- **Request Body**:
  ```json
  {
    "rainfall_mm": 750,
    "temperature_c": 28,
    "soil_ph": 6.5,
    "soil_moisture_pct": 45,
    "fertilizer_kg_per_hectare": 80,
    "irrigation_level_pct": 60,
    "language": "en"
  }
  ```
- **Response**: Returns predicted numerical yield, categorical rating (e.g., "good"), farmer-friendly text interpretation, and actionable recommendations.

### 3. What-If Simulator
**`POST /api/simulate-yield`**
Compares original farming conditions with proposed modifications (e.g., adding more fertilizer).
- **Request Body**: Takes the original prediction parameters and a set of `simulated_*` override parameters.
- **Response**: Returns original yield, simulated yield, percentage change, and a comparative summary.

### 4. Risk Alerts
**`POST /api/risk-alerts`**
Analyzes current parameters and issues warnings for Drought Risk, Crop Stress, Disease Probability, and Flood Risk.
- **Response**: List of generated alerts with severity levels (Low, Medium, High, Critical) and mitigation recommendations.

### 5. Heatmap Generation
**`GET /api/yield-heatmap`**
Returns simulated geographical yield data across 20 districts in Karnataka.
- **Response**: Array of zones with `latitude`, `longitude`, and `yield_label` (High, Medium, Low Yield) along with color codes for UI mapping.

### 6. Soil Analysis
**`POST /api/soil-analysis`**
Assesses soil health.
- **Request Body**: Requires `soil_ph` and `soil_moisture_pct`.
- **Response**: Returns soil quality status, recommended crops, and soil treatment recommendations (e.g., applying lime or gypsum).

### 7. Disease Detection
**`POST /api/disease-detection`**
Accepts a photo of a crop and returns a disease diagnosis. (Designed to be hooked up to a CNN model).
- **Request**: `multipart/form-data` with an `image` file.
- **Response**: Disease name, confidence score, description, and treatment suggestions.

### 8. Government Schemes
**`GET /api/schemes`**
Lists available agricultural schemes like PM-KISAN, PMFBY, and Soil Health Card.

**`POST /api/check-eligibility`**
Checks if a farmer qualifies for schemes based on their profile.
- **Request Body**: `{ "age": 35, "land_holding_hectares": 1.5, "is_farmer": true, "state": "Karnataka", "has_crop": true }`

### 9. Communication & NLP
**`POST /api/chat`**
Accepts a natural language string (e.g., "how is the weather for my crop?") and returns a targeted response using intent detection.

**`POST /api/webhook/sms`**
Configurable webhook URL for Twilio to process incoming SMS commands. Automatically responds to queries like `YIELD 750 28 6.5 45 80 60` or `SOIL 6.5 45`.
