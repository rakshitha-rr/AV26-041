"""
Knowledge Garden — A multilingual dictionary of farming terms.
"""

from typing import List, Dict

FARMING_TERMS: List[Dict] = [
    {
        "id": "npk",
        "name": {"en": "NPK", "hi": "एनपीके", "kn": "ಎನ್.ಪಿ.ಕೆ"},
        "definition": {
            "en": "Short for Nitrogen, Phosphorus, and Potassium, the three primary nutrients crops need to grow.",
            "hi": "नाइट्रोजन, फास्फोरस और पोटेशियम का संक्षिप्त रूप, वे तीन प्राथमिक पोषक तत्व जिनकी फसलों को बढ़ने के लिए आवश्यकता होती है।",
            "kn": "ಸಾರಜನಕ, ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಮ್‌ನ ಸಂಕ್ಷಿಪ್ತ ರೂಪ, ಬೆಳೆಗಳು ಬೆಳೆಯಲು ಅಗತ್ಯವಿರುವ ಮೂರು ಪ್ರಾಥಮಿಕ ಪೋಷಕಾಂಶಗಳು."
        },
        "category": "Fertilizer"
    },
    {
        "id": "soil_ph",
        "name": {"en": "Soil pH", "hi": "मिट्टी का पीएच", "kn": "ಮಣ್ಣಿನ ಪಿಹೆಚ್"},
        "definition": {
            "en": "A measure of how acidic or alkaline the soil is. Most crops grow best in pH 6.0 to 7.5.",
            "hi": "मिट्टी कितनी अम्लीय या क्षारीय है इसका माप। अधिकांश फसलें पीएच 6.0 से 7.5 में सबसे अच्छी बढ़ती हैं।",
            "kn": "ಮಣ್ಣು ಎಷ್ಟು ಆಮ್ಲೀಯ ಅಥವಾ ಕ್ಷಾರೀಯವಾಗಿದೆ ಎಂಬುದರ ಅಳತೆ. ಹೆಚ್ಚಿನ ಬೆಳೆಗಳು 6.0 ರಿಂದ 7.5 pH ನಲ್ಲಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯುತ್ತವೆ."
        },
        "category": "Soil Health"
    },
    {
        "id": "irrigation",
        "name": {"en": "Irrigation", "hi": "सिंचाई", "kn": "ನೀರಾವರಿ"},
        "definition": {
            "en": "The artificial application of water to land to assist in the production of crops.",
            "hi": "फसलों के उत्पादन में सहायता के लिए भूमि पर पानी का कृत्रिम प्रयोग।",
            "kn": "ಬೆಳೆಗಳ ಉತ್ಪಾದನೆಗೆ ಸಹಾಯ ಮಾಡಲು ಭೂಮಿಗೆ ಕೃತಕವಾಗಿ ನೀರನ್ನು ಒದಗಿಸುವುದು."
        },
        "category": "Water Management"
    },
    {
        "id": "crop_rotation",
        "name": {"en": "Crop Rotation", "hi": "फसल चक्र", "kn": "ಬೆಳೆ ಸರದಿ"},
        "definition": {
            "en": "Growing different crops in the same area in sequential seasons to improve soil health and control pests.",
            "hi": "मिट्टी के स्वास्थ्य में सुधार और कीटों को नियंत्रित करने के लिए अनुक्रमिक मौसमों में एक ही क्षेत्र में अलग-अलग फसलें उगाना।",
            "kn": "ಮಣ್ಣಿನ ಆರೋಗ್ಯವನ್ನು ಸುಧಾರಿಸಲು ಮತ್ತು ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸಲು ಒಂದೇ ಪ್ರದೇಶದಲ್ಲಿ ಅನುಕ್ರಮ ಋತುಗಳಲ್ಲಿ ವಿವಿಧ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುವುದು."
        },
        "category": "Technique"
    },
    {
        "id": "vermicompost",
        "name": {"en": "Vermicompost", "hi": "वर्मीकम्पोस्ट", "kn": "ರೋಗಮುಕ್ತ ಗೊಬ್ಬರ"},
        "definition": {
            "en": "Organic fertilizer produced by earthworms decomposing organic waste.",
            "hi": "केंचुओं द्वारा जैविक कचरे के अपघटन से निर्मित जैविक खाद।",
            "kn": "ಎರೆಹುಳುಗಳು ಸಾವಯವ ತ್ಯಾಜ್ಯವನ್ನು ಕೊಳೆಸುವ ಮೂಲಕ ಉತ್ಪಾದಿಸುವ ಸಾವಯವ ಗೊಬ್ಬರ."
        },
        "category": "Fertilizer"
    },
    {
        "id": "mulching",
        "name": {"en": "Mulching", "hi": "मल्चिंग", "kn": "ಹೊದಿಕೆ ಹಾಕುವಿಕೆ"},
        "definition": {
            "en": "Covering the soil surface around plants with straw or plastic to retain moisture and suppress weeds.",
            "hi": "नमी बनाए रखने और खरपतवारों को दबाने के लिए पौधों के आसपास की मिट्टी की सतह को पुआल या प्लास्टिक से ढंकना।",
            "kn": "ತೇವಾಂಶವನ್ನು ಉಳಿಸಿಕೊಳ್ಳಲು ಮತ್ತು ಕಳೆಗಳನ್ನು ಹತ್ತಿಕ್ಕಲು ಸಸ್ಯಗಳ ಸುತ್ತಲಿನ ಮಣ್ಣಿನ ಮೇಲ್ಮೈಯನ್ನು ಒಣಹುಲ್ಲು ಅಥವಾ ಪ್ಲಾಸ್ಟಿಕ್‌ನಿಂದ ಮುಚ್ಚುವುದು."
        },
        "category": "Technique"
    },
    {
        "id": "kharif",
        "name": {"en": "Kharif", "hi": "खरीफ", "kn": "ಖಾರಿಫ್"},
        "definition": {
            "en": "Crops sown at the beginning of the monsoon season (June/July) and harvested in autumn (September/October).",
            "hi": "मानसून के मौसम (जून/जुलाई) की शुरुआत में बोई जाने वाली और शरद ऋतु (सितंबर/अक्टूबर) में काटी जाने वाली फसलें।",
            "kn": "ಮುಂಗಾರು ಹಂಗಾಮಿನ ಆರಂಭದಲ್ಲಿ (ಜೂನ್/ಜುಲೈ) ಬಿತ್ತನೆ ಮಾಡಿ ಶರತ್ಕಾಲದಲ್ಲಿ (ಸೆಪ್ಟೆಂಬರ್/ಅಕ್ಟೋಬರ್) ಕೊಯ್ಲು ಮಾಡುವ ಬೆಳೆಗಳು."
        },
        "category": "Season"
    },
    {
        "id": "rabi",
        "name": {"en": "Rabi", "hi": "रबी", "kn": "ರಬಿ"},
        "definition": {
            "en": "Crops sown in winter (October/November) and harvested in spring (March/April).",
            "hi": "सर्दियों (अक्टूबर/नवंबर) में बोई जाने वाली और वसंत (मार्च/अप्रैल) में काटी जाने वाली फसलें।",
            "kn": "ಚಳಿಗಾಲದಲ್ಲಿ (ಅಕ್ಟೋಬರ್/ನವೆಂಬರ್) ಬಿತ್ತನೆ ಮಾಡಿ ವಸಂತಕಾಲದಲ್ಲಿ (ಮಾರ್ಚ್/ಏಪ್ರಿಲ್) ಕೊಯ್ಲು ಮಾಡುವ ಬೆಳೆಗಳು."
        },
        "category": "Season"
    }
]

def get_all_farming_terms() -> List[Dict]:
    """Returns the complete farming dictionary with all translations."""
    return FARMING_TERMS
