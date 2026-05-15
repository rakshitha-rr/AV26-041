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
├── models/
│   ├── schemas.py          # Pydantic models for API validation
│   ├── yield_model.py      # RandomForest ML model for yield prediction
│   └── risk_model.py       # Rule-based engine for detecting risks
├── routes/
│   ├── auth.py             # Farmer Aadhaar Login
│   ├── prediction.py       # Core Yield Prediction
│   ├── simulation.py       # What-If Simulator
│   ├── risk_alerts.py      # Climate & Stress alerts
│   ├── sms.py              # NEW: Real SMS & Call handling (Twilio)
│   ├── knowledge.py        # NEW: Agri Dictionary (Knowledge Garden)
│   ├── voice.py            # Multilingual Voice Assistant integration
│   ├── soil.py             # Soil analysis
│   ├── schemes.py          # Gov schemes
│   └── heatmap.py          # Zone-wise yield generation
└── utils/
    ├── interpreter.py      # Numerical to text converter
    ├── knowledge.py        # Dictionary data and search logic
    ├── sms_handler.py      # Twilio integration & SMS NLP
    ├── text_to_speech.py   # Google TTS integration
    └── speech_to_text.py   # Google Speech API integration
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

### 9. SMS & Call Center
**`POST /api/send-sms`**
Manually send an SMS to a farmer.
- **Request Body**:
  ```json
  {
    "message": "Your yield prediction is moderate. Add fertilizer.",
    "phone_number": "+919916721196"
  }
  ```

**`POST /api/call`**
Initiate an outbound voice call to a farmer. Plays a welcome message and connects to support.
- **Request Body**: `{ "to_number": "+919916721196" }`

**`POST /api/webhook/sms`**
Twilio Webhook for incoming SMS. Automatically parses commands and runs ML models.
- **Commands**:
  - `YIELD <rain> <temp> <ph> <moist> <fert> <irr>`: Returns yield prediction.
  - `SOIL <ph> <moist>`: Returns soil quality analysis.
  - `RISK <params>`: Returns risk level and alerts.
  - `AA#...#END`: Proprietary offline protocol for soil data.
  - `HELP`: Lists available commands.

**`POST /api/webhook/voice`**
Twilio Webhook for incoming calls. Greets the farmer and forwards the call to the support team.

---

### 10. Voice AI Assistant
**`POST /api/voice/voice-assistant`**
The main interactive voice interface. Transcribes audio, determines intent (including Knowledge Garden lookups), and returns speech.
- **Response**: Returns transcription, text response, and `audio_url`.

**`POST /api/voice/voice-output`**
Converts text to an audio speech file.
- **Input**: `{ "text": "...", "language": "en" }`
- **Output**: `{ "audio_url": "..." }`

---

### 11. Knowledge Garden (Agri Dictionary)
**`GET /api/knowledge-garden`**
Returns the complete multilingual dictionary of farming terms.

**`GET /api/knowledge`**
Fetches specific term details (Definition, Usage, Simple Explanation).
- **Query Param**: `term` (ID or name)

**`GET /api/knowledge/search`**
Partial name matching search.
- **Query Param**: `query`

**`GET /api/knowledge/suggestions`**
Returns a list of all term names for autocomplete.

**`GET /api/knowledge/voice`**
Generates speech for a term's **Simple Explanation** in the selected language.
- **Query Params**: `term_id`, `language`
- **Response**: `{ "audio_url": "..." }`
