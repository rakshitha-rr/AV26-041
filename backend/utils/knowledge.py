"""
Knowledge Garden — A multilingual dictionary of farming terms.
"""

from typing import List, Dict, Optional

FARMING_TERMS: List[Dict] = [
    {
        "id": "npk",
        "name": {"en": "NPK", "hi": "एनपीके", "kn": "ಎನ್.ಪಿ.ಕೆ"},
        "definition": {
            "en": "Short for Nitrogen, Phosphorus, and Potassium, the three primary nutrients crops need to grow.",
            "hi": "नाइट्रोजन, फास्फोरस और पोटेशियम का संक्षिप्त रूप, वे तीन प्राथमिक पोषक तत्व जिनकी फसलों को बढ़ने के लिए आवश्यकता होती है।",
            "kn": "ಸಾರಜನಕ, ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಮ್‌ನ ಸಂಕ್ಷಿಪ್ತ ರೂಪ, ಬೆಳೆಗಳು ಬೆಳೆಯಲು ಅಗತ್ಯವಿರುವ ಮೂರು ಪ್ರಾಥಮಿಕ ಪೋಷಕಾಂಶಗಳು."
        },
        "usage": {
            "en": "Apply balanced NPK fertilizer based on soil test results.",
            "hi": "मिट्टी परीक्षण के परिणामों के आधार पर संतुलित एनपीके उर्वरक डालें।",
            "kn": "ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ ಫಲಿತಾಂಶಗಳ ಆಧಾರದ ಮೇಲೆ ಸಮತೋಲಿತ ಎನ್.ಪಿ.ಕೆ ಗೊಬ್ಬರವನ್ನು ಅನ್ವಯಿಸಿ."
        },
        "simple": {
            "en": "Three main foods that plants eat to grow big and healthy.",
            "hi": "पौधों के बढ़ने और स्वस्थ रहने के लिए तीन मुख्य भोजन।",
            "kn": "ಸಸ್ಯಗಳು ದೊಡ್ಡದಾಗಿ ಮತ್ತು ಆರೋಗ್ಯಕರವಾಗಿ ಬೆಳೆಯಲು ತಿನ್ನುವ ಮೂರು ಮುಖ್ಯ ಆಹಾರಗಳು."
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
        "usage": {
            "en": "Check soil pH every season to determine if lime or sulfur is needed.",
            "hi": "हर मौसम में मिट्टी के पीएच की जांच करें ताकि यह पता चल सके कि चूने या सल्फर की आवश्यकता है या नहीं।",
            "kn": "ಸುಣ್ಣ ಅಥವಾ ಗಂಧಕದ ಅಗತ್ಯವಿದೆಯೇ ಎಂದು ನಿರ್ಧರಿಸಲು ಪ್ರತಿ ಹಂಗಾಮಿನಲ್ಲಿ ಮಣ್ಣಿನ ಪಿಹೆಚ್ ಪರೀಕ್ಷಿಸಿ."
        },
        "simple": {
            "en": "Tells you if your soil is like a lemon (acidic) or like soap (alkaline).",
            "hi": "आपको बताता है कि आपकी मिट्टी नींबू (अम्लीय) की तरह है या साबुन (क्षारीय) की तरह।",
            "kn": "ನಿಮ್ಮ ಮಣ್ಣು ನಿಂಬೆಯಂತೆ (ಆಮ್ಲೀಯ) ಅಥವಾ ಸಾಬೂನಿನಂತೆ (ಕ್ಷಾರೀಯ) ಇದೆಯೇ ಎಂದು ನಿಮಗೆ ತಿಳಿಸುತ್ತದೆ."
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
        "usage": {
            "en": "Use drip irrigation to save water and deliver it directly to roots.",
            "hi": "पानी बचाने और उसे सीधे जड़ों तक पहुँचाने के लिए ड्रिप सिंचाई का उपयोग करें।",
            "kn": "ನೀರನ್ನು ಉಳಿಸಲು ಮತ್ತು ನೇರವಾಗಿ ಬೇರುಗಳಿಗೆ ತಲುಪಿಸಲು ಹನಿ ನೀರಾವರಿ ಬಳಸಿ."
        },
        "simple": {
            "en": "Giving water to plants when there is no rain.",
            "hi": "बारिश न होने पर पौधों को पानी देना।",
            "kn": "ಮಳೆ ಇಲ್ಲದಿದ್ದಾಗ ಸಸ್ಯಗಳಿಗೆ ನೀರು ಕೊಡುವುದು."
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
        "usage": {
            "en": "Rotate legumes with cereals to naturally increase nitrogen in the soil.",
            "hi": "मिट्टी में स्वाभाविक रूप से नाइट्रोजन बढ़ाने के लिए अनाज के साथ फलियों को बदलें।",
            "kn": "ಮಣ್ಣಿನಲ್ಲಿ ಸಾರಜನಕವನ್ನು ನೈಸರ್ಗಿಕವಾಗಿ ಹೆಚ್ಚಿಸಲು ಧಾನ್ಯಗಳೊಂದಿಗೆ ದ್ವಿದಳ ಧಾನ್ಯಗಳನ್ನು ಬೆರೆಸಿ ಬೆಳೆಯಿರಿ."
        },
        "simple": {
            "en": "Changing what you grow every year so the soil stays strong and pests get confused.",
            "hi": "हर साल आप जो उगाते हैं उसे बदलना ताकि मिट्टी मजबूत रहे और कीट भ्रमित हो जाएं।",
            "kn": "ಪ್ರತಿ ವರ್ಷ ನೀವು ಬೆಳೆಯುವುದನ್ನು ಬದಲಾಯಿಸುವುದು ಇದರಿಂದ ಮಣ್ಣು ಬಲವಾಗಿರುತ್ತದೆ ಮತ್ತು ಕೀಟಗಳು ಗೊಂದಲಕ್ಕೊಳಗಾಗುತ್ತವೆ."
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
        "usage": {
            "en": "Mix vermicompost into the soil during land preparation.",
            "hi": "भूमि की तैयारी के दौरान मिट्टी में वर्मीकम्पोस्ट मिलाएं।",
            "kn": "ಭೂಮಿ ಸಿದ್ಧಪಡಿಸುವಾಗ ಮಣ್ಣಿನಲ್ಲಿ ಎರೆಹುಳು ಗೊಬ್ಬರವನ್ನು ಬೆರೆಸಿ."
        },
        "simple": {
            "en": "Special soil made by earthworms that is like vitamins for plants.",
            "hi": "केंचुओं द्वारा बनाई गई विशेष मिट्टी जो पौधों के लिए विटामिन की तरह है।",
            "kn": "ಎರೆಹುಳುಗಳು ತಯಾರಿಸಿದ ವಿಶೇಷ ಮಣ್ಣು ಸಸ್ಯಗಳಿಗೆ ಜೀವಸತ್ವಗಳಂತೆ ಇರುತ್ತದೆ."
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
        "usage": {
            "en": "Apply a thick layer of straw mulch to reduce evaporation.",
            "hi": "वाष्पीकरण को कम करने के लिए पुआल गीली घास की एक मोटी परत लगाएं।",
            "kn": "ಬಾಷ್ಪೀಕರಣವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಒಣಹುಲ್ಲಿನ ಮಲ್ಚ್‌ನ ದಪ್ಪ ಪದರವನ್ನು ಅನ್ವಯಿಸಿ."
        },
        "simple": {
            "en": "Putting a 'blanket' on the soil to keep it cool, wet, and weed-free.",
            "hi": "मिट्टी को ठंडा, गीला और खरपतवार मुक्त रखने के लिए उस पर 'कंबल' डालना।",
            "kn": "ಮಣ್ಣನ್ನು ತಂಪಾಗಿ, ತೇವವಾಗಿ ಮತ್ತು ಕಳೆ ರಹಿತವಾಗಿಡಲು ಅದರ ಮೇಲೆ 'ಬದಲಿ ಹೊದಿಕೆ' ಹಾಕುವುದು."
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
        "usage": {
            "en": "Rice, maize, and cotton are common Kharif crops in Karnataka.",
            "hi": "चावल, मक्का और कपास कर्नाटक में आम खरीफ फसलें हैं।",
            "kn": "ಭತ್ತ, ಮೆಕ್ಕೆಜೋಳ ಮತ್ತು ಹತ್ತಿ ಕರ್ನಾಟಕದ ಸಾಮಾನ್ಯ ಖಾರಿಫ್ ಬೆಳೆಗಳು."
        },
        "simple": {
            "en": "Crops grown during the rainy season.",
            "hi": "बारिश के मौसम में उगाई जाने वाली फसलें।",
            "kn": "ಮಳೆಗಾಲದಲ್ಲಿ ಬೆಳೆಯುವ ಬೆಳೆಗಳು."
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
        "usage": {
            "en": "Wheat and mustard are popular Rabi crops.",
            "hi": "गेहूं और सरसों लोकप्रिय रबी फसलें हैं।",
            "kn": "ಗೋಧಿ ಮತ್ತು ಸಾಸಿವೆ ಜನಪ್ರಿಯ ರಬಿ ಬೆಳೆಗಳು."
        },
        "simple": {
            "en": "Crops grown during the winter season.",
            "hi": "सर्दियों के मौसम में उगाई जाने वाली फसलें।",
            "kn": "ಚಳಿಗಾಲದಲ್ಲಿ ಬೆಳೆಯುವ ಬೆಳೆಗಳು."
        },
        "category": "Season"
    },
    {
        "id": "pesticide",
        "name": {"en": "Pesticide", "hi": "कीटनाशक", "kn": "ಕೀಟನಾಶಕ"},
        "definition": {
            "en": "A substance used for destroying insects or other organisms harmful to cultivated plants.",
            "hi": "खेती वाले पौधों के लिए हानिकारक कीड़ों या अन्य जीवों को नष्ट करने के लिए इस्तेमाल किया जाने वाला पदार्थ।",
            "kn": "ಬೆಳೆಸಿದ ಸಸ್ಯಗಳಿಗೆ ಹಾನಿಕಾರಕ ಕೀಟಗಳು ಅಥವಾ ಇತರ ಜೀವಿಗಳನ್ನು ನಾಶಮಾಡಲು ಬಳಸುವ ವಸ್ತು."
        },
        "usage": {
            "en": "Only use pesticides as a last resort and follow safety guidelines.",
            "hi": "केवल अंतिम उपाय के रूप में कीटनाशकों का उपयोग करें और सुरक्षा दिशानिर्देशों का पालन करें।",
            "kn": "ಕೊನೆಯ ಉಪಾಯವಾಗಿ ಮಾತ್ರ ಕೀಟನಾಶಕಗಳನ್ನು ಬಳಸಿ ಮತ್ತು ಸುರಕ್ಷತಾ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಅನುಸರಿಸಿ."
        },
        "simple": {
            "en": "Medicine for plants to kill bad bugs.",
            "hi": "बुरे कीड़ों को मारने के लिए पौधों की दवा।",
            "kn": "ಕೆಟ್ಟ ಕೀಟಗಳನ್ನು ಕೊಲ್ಲಲು ಸಸ್ಯಗಳಿಗೆ ನೀಡುವ ಔಷಧಿ."
        },
        "category": "Protection"
    },
    {
        "id": "urea",
        "name": {"en": "Urea", "hi": "यूरिया", "kn": "ಯೂರಿಯಾ"},
        "definition": {
            "en": "A widely used solid nitrogen fertilizer that helps plants grow green and leafy.",
            "hi": "एक व्यापक रूप से इस्तेमाल किया जाने वाला ठोस नाइट्रोजन उर्वरक जो पौधों को हरा और पत्तेदार बनाने में मदद करता है।",
            "kn": "ವ್ಯಾಪಕವಾಗಿ ಬಳಸಲಾಗುವ ಘನ ಸಾರಜನಕ ಗೊಬ್ಬರ ಇದು ಸಸ್ಯಗಳು ಹಸಿರಾಗಿ ಬೆಳೆಯಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ."
        },
        "usage": {
            "en": "Apply in split doses during the active growth phase of the crop.",
            "hi": "फसल के सक्रिय विकास चरण के दौरान विभाजित खुराक में लागू करें।",
            "kn": "ಬೆಳೆಯ ಸಕ್ರಿಯ ಬೆಳವಣಿಗೆಯ ಹಂತದಲ್ಲಿ ವಿಭಜಿತ ಪ್ರಮಾಣದಲ್ಲಿ ಅನ್ವಯಿಸಿ."
        },
        "simple": {
            "en": "A special white powder that gives plants a big boost of energy to grow leaves.",
            "hi": "एक विशेष सफेद पाउडर जो पौधों को पत्तियां उगाने के लिए ऊर्जा देता है।",
            "kn": "ಸಸ್ಯಗಳಿಗೆ ಎಲೆಗಳನ್ನು ಬೆಳೆಯಲು ಶಕ್ತಿ ನೀಡುವ ವಿಶೇಷ ಬಿಳಿ ಪುಡಿ."
        },
        "category": "Fertilizer"
    },
    {
        "id": "yield",
        "name": {"en": "Crop Yield", "hi": "फसल की पैदावार", "kn": "ಬೆಳೆ ಇಳುವರಿ"},
        "definition": {
            "en": "A measurement of the amount of agricultural production harvested per unit of land area.",
            "hi": "प्रति इकाई भूमि क्षेत्र में काटी गई कृषि उपज की मात्रा का माप।",
            "kn": "ಪ್ರತಿ ಘಟಕ ಭೂಪ್ರದೇಶದಲ್ಲಿ ಕಟಾವು ಮಾಡಿದ ಕೃಷಿ ಉತ್ಪಾದನೆಯ ಪ್ರಮಾಣದ ಅಳತೆ."
        },
        "usage": {
            "en": "Use the yield prediction tool to estimate harvest volume before the season ends.",
            "hi": "मौसम समाप्त होने से पहले फसल की मात्रा का अनुमान लगाने के लिए उपज भविष्यवाणी उपकरण का उपयोग करें।",
            "kn": "ಹಂಗಾಮು ಮುಗಿಯುವ ಮೊದಲು ಕಟಾವಿನ ಪ್ರಮಾಣವನ್ನು ಅಂದಾಜು ಮಾಡಲು ಇಳುವರಿ ಮುನ್ಸೂಚನೆ ಉಪಕರಣ ಬಳಸಿ."
        },
        "simple": {
            "en": "How much food or crops you get from your farm at harvest time.",
            "hi": "फसल के समय आपको अपने खेत से कितना भोजन या फसल मिलती है।",
            "kn": "ಕಟಾವಿನ ಸಮಯದಲ್ಲಿ ನಿಮ್ಮ ಜಮೀನಿನಿಂದ ನೀವು ಎಷ್ಟು ಆಹಾರ ಅಥವಾ ಬೆಳೆಗಳನ್ನು ಪಡೆಯುತ್ತೀರಿ."
        },
        "category": "Harvest"
    },
    {
        "id": "drought",
        "name": {"en": "Drought", "hi": "सूखा", "kn": "ಬರ"},
        "definition": {
            "en": "A prolonged period of abnormally low rainfall, leading to a shortage of water.",
            "hi": "असामान्य रूप से कम वर्षा की लंबी अवधि, जिससे पानी की कमी हो जाती है।",
            "kn": "ಅಸಹಜವಾಗಿ ಕಡಿಮೆ ಮಳೆಯ ದೀರ್ಘಾವಧಿ, ಇದು ನೀರಿನ ಕೊರತೆಗೆ ಕಾರಣವಾಗುತ್ತದೆ."
        },
        "usage": {
            "en": "Implement water conservation techniques like mulching during drought conditions.",
            "hi": "सूखे की स्थिति के दौरान मल्चिंग जैसी जल संरक्षण तकनीकों को लागू करें।",
            "kn": "ಬರಗಾಲದ ಪರಿಸ್ಥಿತಿಯಲ್ಲಿ ಮಲ್ಚಿಂಗ್ ನಂತಹ ಜಲ ಸಂರಕ್ಷಣೆ ತಂತ್ರಗಳನ್ನು ಅಳವಡಿಸಿಕೊಳ್ಳಿ."
        },
        "simple": {
            "en": "When it doesn't rain for a very long time and the ground gets very dry.",
            "hi": "जब बहुत लंबे समय तक बारिश नहीं होती है और जमीन बहुत सूखी हो जाती है।",
            "kn": "ತುಂಬಾ ಸಮಯ ಮಳೆ ಬಾರದೆ ನೆಲ ತುಂಬಾ ಒಣಗಿದಾಗ."
        },
        "category": "Weather"
    }
]

def get_all_farming_terms() -> List[Dict]:
    """Returns the complete farming dictionary with all translations."""
    return FARMING_TERMS

def get_term_by_id(term_id: str) -> Optional[Dict]:
    """Get term by its unique ID."""
    return next((t for t in FARMING_TERMS if t["id"] == term_id.lower()), None)

def search_terms(query: str, language: str = "en") -> List[Dict]:
    """Search for terms by name across languages."""
    query = query.lower().strip()
    matches = []
    for term in FARMING_TERMS:
        # Check if query matches name in any language or ID
        if (query in term["id"] or 
            query in term["name"].get("en", "").lower() or 
            query in term["name"].get("hi", "").lower() or 
            query in term["name"].get("kn", "").lower()):
            matches.append(term)
    return matches

def get_term_suggestions() -> List[str]:
    """Get a list of all term names in English."""
    return [term["name"]["en"] for term in FARMING_TERMS]
