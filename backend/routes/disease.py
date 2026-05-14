"""
Disease Detection Route — Accepts crop image and returns disease diagnosis.
POST /disease-detection
Designed to be extendable for CNN-based models.
"""

import random
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import DiseaseDetectionResponse

router = APIRouter(tags=["🦠 Disease Detection"])

# Mock disease database (extendable with CNN model)
DISEASE_DATABASE = [
    {
        "name": "Rice Blast",
        "description": "Fungal disease causing diamond-shaped lesions on leaves. Common in humid conditions.",
        "suggestions": [
            "Apply Tricyclazole fungicide at 0.6g/litre",
            "Drain excess water from fields",
            "Use blast-resistant rice varieties like IR64",
            "Avoid excess nitrogen fertilizer",
        ],
    },
    {
        "name": "Leaf Blight",
        "description": "Bacterial/fungal infection causing yellowing and drying of leaf tips and margins.",
        "suggestions": [
            "Apply Copper Oxychloride spray",
            "Remove and destroy infected plant debris",
            "Ensure proper spacing between plants",
            "Use certified disease-free seeds",
        ],
    },
    {
        "name": "Rust (Wheat/Ragi)",
        "description": "Fungal disease showing orange-brown pustules on leaves and stems.",
        "suggestions": [
            "Apply Mancozeb or Propiconazole fungicide",
            "Plant rust-resistant crop varieties",
            "Avoid late sowing",
            "Monitor fields weekly during humid weather",
        ],
    },
    {
        "name": "Wilt Disease",
        "description": "Soil-borne fungal infection causing wilting and yellowing of entire plant.",
        "suggestions": [
            "Practice crop rotation with non-host crops",
            "Apply Trichoderma bio-fungicide to soil",
            "Improve soil drainage",
            "Use wilt-resistant crop varieties",
        ],
    },
    {
        "name": "Healthy Plant",
        "description": "No disease symptoms detected. The crop appears healthy.",
        "suggestions": [
            "Continue current farming practices",
            "Monitor regularly for early symptoms",
            "Maintain proper nutrition and irrigation",
        ],
    },
]


@router.post("/disease-detection", response_model=DiseaseDetectionResponse)
async def detect_disease(image: UploadFile = File(...)):
    """
    Accept a crop image and return disease diagnosis.
    Currently uses rule-based simulation — designed for CNN model integration.
    """
    try:
        # Validate file type
        allowed = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if image.content_type not in allowed:
            raise HTTPException(status_code=400, detail=f"Invalid image type: {image.content_type}. Use JPEG/PNG.")

        # Read image (for future CNN processing)
        contents = await image.read()
        file_size_kb = len(contents) / 1024

        if file_size_kb < 1:
            raise HTTPException(status_code=400, detail="Image too small. Please upload a clear crop photo.")

        # Simulate disease detection (replace with CNN model inference)
        # In production: preprocess image → load model → predict
        disease = random.choice(DISEASE_DATABASE)
        is_healthy = disease["name"] == "Healthy Plant"
        confidence = round(random.uniform(0.75, 0.95), 2) if not is_healthy else round(random.uniform(0.85, 0.98), 2)

        return DiseaseDetectionResponse(
            disease_detected=not is_healthy,
            disease_name=disease["name"],
            confidence=confidence,
            description=disease["description"],
            suggestions=disease["suggestions"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease detection failed: {str(e)}")
