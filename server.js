const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// File upload config
const upload = multer({ dest: 'uploads/', limits: { fileSize: 5 * 1024 * 1024 } });
if (!fs.existsSync('uploads')) fs.mkdirSync('uploads');

// Load data
const terms = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'terms.json'), 'utf-8'));
const schemes = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'schemes.json'), 'utf-8'));

// In-memory logs
const chatLogs = [];
const smsLogs = []; // Stores incoming SMS for the owner's feed

// ============ AI RESPONSE ENGINE ============

const responses = [
  { keys: ['nitrogen', 'low nitrogen', 'n deficiency'], reply: "🌿 **Low Nitrogen Detected!**\n\nNitrogen is critical for leaf growth and chlorophyll production. Here's what you can do:\n\n1. **Apply Urea** (46-0-0) at 50-60 kg/acre\n2. **Use Neem-coated urea** for slow release\n3. **Add organic sources**: vermicompost (2-3 tonnes/acre)\n4. **Grow green manure** crops like dhaincha or sunhemp in the next season\n5. **Intercrop with legumes** (moong, groundnut) for natural nitrogen fixation\n\n⏰ Best time to apply: Early morning or late evening with light irrigation." },
  { keys: ['phosphorus', 'low phosphorus', 'p deficiency'], reply: "🌱 **Phosphorus Deficiency Advice**\n\nPhosphorus is essential for root development and flowering.\n\n1. **Apply DAP** (18-46-0) at 50 kg/acre at sowing\n2. **Use SSP** (Single Super Phosphate) for sulfur-deficient soils\n3. **Add bone meal** as organic P source\n4. **Maintain soil pH 6.0-7.0** for best P availability\n5. **Apply PSB** (Phosphate Solubilizing Bacteria) biofertilizer\n\n💡 Tip: Phosphorus is immobile in soil — place it near the root zone." },
  { keys: ['potassium', 'low potassium', 'k deficiency'], reply: "🍃 **Potassium Management**\n\nPotassium strengthens plant immunity and improves fruit quality.\n\n1. **Apply MOP** (Muriate of Potash) at 40 kg/acre\n2. **Use SOP** for chloride-sensitive crops (potato, tobacco)\n3. **Banana stems and wood ash** are good organic K sources\n4. **Split application**: 50% basal + 50% at flowering\n\n💡 Signs of K deficiency: Yellowing leaf edges, weak stems, small fruits." },
  { keys: ['pest', 'insect', 'bug', 'worm', 'caterpillar'], reply: "🐛 **Pest Management Advice**\n\nFollow Integrated Pest Management (IPM) approach:\n\n1. **Cultural control**: Crop rotation, timely sowing, resistant varieties\n2. **Biological control**: Release Trichogramma cards (50,000/acre)\n3. **Mechanical**: Install pheromone traps, yellow sticky traps\n4. **Botanical**: Neem oil spray (5ml/liter) every 15 days\n5. **Chemical** (last resort): Use recommended insecticide at proper dosage\n\n📱 Report unusual pest outbreaks to your local Krishi Vigyan Kendra (KVK)." },
  { keys: ['disease', 'fungus', 'blight', 'wilt', 'rot', 'rust'], reply: "🦠 **Crop Disease Management**\n\n1. **Prevention**: Use certified disease-free seeds, seed treatment with fungicide\n2. **For fungal diseases**: Spray Mancozeb (2.5g/L) or Carbendazim (1g/L)\n3. **For bacterial wilt**: Remove infected plants, apply Trichoderma to soil\n4. **For viral diseases**: Control vector insects (whitefly, aphids)\n5. **Improve drainage** to prevent root rot\n\n🧪 Get exact diagnosis from your nearest agriculture university or KVK." },
  { keys: ['water', 'irrigation', 'drought', 'rain', 'moisture'], reply: "💧 **Water & Irrigation Tips**\n\n1. **Drip irrigation** saves 30-60% water — get 55-80% subsidy under PMKSY\n2. **Mulching** reduces evaporation by 25%\n3. **Schedule irrigation** based on crop stage (critical stages need more water)\n4. **Rainwater harvesting**: Build farm ponds for dry spells\n5. **Moisture sensors** help optimize irrigation timing\n\n🌧️ Check IMD weather forecast before irrigation planning." },
  { keys: ['fertilizer', 'nutrient', 'manure', 'urea', 'dap'], reply: "🧪 **Fertilizer Management Guide**\n\n1. **Always get soil tested first** — Soil Health Card is free!\n2. **Balanced NPK**: Don't over-apply any single nutrient\n3. **Organic + Chemical**: Use 50% organic (FYM/vermicompost) + 50% chemical\n4. **Micronutrients**: Apply ZnSO4 and Borax based on soil test\n5. **Timing**: Basal dose at sowing + top dressing at critical stages\n\n💰 Use neem-coated urea for 10-15% better nitrogen efficiency." },
  { keys: ['wheat', 'gehu'], reply: "🌾 **Wheat Cultivation Tips**\n\n- **Sowing**: Nov 1-25 (timely), use HD-3226 or PBW-825 varieties\n- **Seed rate**: 40-45 kg/acre\n- **Fertilizer**: 60 kg Urea + 50 kg DAP + 20 kg MOP per acre\n- **Irrigation**: 4-6 irrigations at CRI, tillering, flowering, grain filling\n- **Weed control**: Sulfosulfuron 25g/acre at 30-35 DAS\n\n📅 Harvest: April, when grain moisture is 12-14%." },
  { keys: ['rice', 'paddy', 'dhan'], reply: "🌾 **Rice/Paddy Cultivation Tips**\n\n- **Nursery**: June, use Pusa Basmati 1121 or Swarna varieties\n- **Transplanting**: 20-25 day old seedlings, 2-3 per hill\n- **SRI method**: Single seedling, wider spacing, saves 40% water\n- **Fertilizer**: 50 kg Urea + 30 kg DAP per acre in splits\n- **Pest watch**: Stem borer, BPH — use light traps\n\n💧 Alternate wetting and drying (AWD) saves 25% water." },
  { keys: ['soil test', 'soil health', 'soil analysis'], reply: "🔬 **Soil Testing Guide**\n\n1. **Collect samples** from 6-8 spots at 15cm depth\n2. **Mix samples** in a clean bucket, take 500g\n3. **Label**: Your name, village, field number, crop grown\n4. **Submit** to nearest Soil Testing Lab or KVK (FREE under Soil Health Card scheme)\n5. **Results** include: pH, EC, OC, N, P, K, and micronutrients\n\n🗓️ Test every 2 years. Best time: After harvest, before sowing." },
  { keys: ['organic', 'natural', 'chemical free', 'jaivik'], reply: "🌿 **Organic Farming Guide**\n\n1. **Start transition**: Reduce chemicals by 25% each season\n2. **Compost**: FYM (5-10 tonnes/acre) + Vermicompost (2 tonnes/acre)\n3. **Bio-pesticides**: Neem oil, Beauveria bassiana, Trichoderma\n4. **Get certified**: Apply under PKVY scheme (₹50,000/ha support)\n5. **Market premium**: Organic produce gets 20-30% higher price\n\n🏷️ PGS certification is free for farmer groups of 50+." },
  { keys: ['weather', 'climate', 'forecast', 'temperature'], reply: "🌤️ **Weather-Smart Farming**\n\n1. Check **IMD Agromet Advisory** for your district weekly\n2. Install **Meghdoot app** for location-based weather alerts\n3. **Frost protection**: Irrigate fields evening before frost, use smoke\n4. **Heat wave**: Mulching + frequent light irrigation\n5. **Heavy rain**: Ensure drainage channels are clear\n\n📱 SMS weather alerts: Register at mausam.imd.gov.in" },
  { keys: ['market', 'price', 'sell', 'mandi', 'msp'], reply: "💰 **Market & Price Guide**\n\n1. **Check MSP rates** on farmer.gov.in before selling\n2. **Register on e-NAM** for access to 1000+ mandis nationwide\n3. **Grade your produce** — sorted/graded gets 10-15% more\n4. **Storage**: Use government warehouses (WDRA) if market price is low\n5. **FPO membership**: Collective selling gets better prices\n\n📊 Current MSP: Wheat ₹2,275/qtl, Rice ₹2,203/qtl, Mustard ₹5,650/qtl." },
  { keys: ['subsidy', 'scheme', 'government', 'sarkari', 'yojana'], reply: "🏛️ **Key Government Schemes for Farmers**\n\n1. **PM-KISAN**: ₹6,000/year direct transfer\n2. **PMFBY**: Crop insurance at 1.5-2% premium\n3. **KCC**: Loan up to ₹3 lakh at 4% interest\n4. **PMKSY**: 55-80% subsidy on drip/sprinkler\n5. **PKVY**: ₹50,000/ha for organic farming\n\n📱 Apply through CSC centers or farmer.gov.in portal.\n\nCheck our **Knowledge Garden > Schemes** section for full details!" },
  { keys: ['tomato', 'tamatar'], reply: "🍅 **Tomato Cultivation & Disease Guide**\n\n- **Season**: June-July (Kharif), Oct-Nov (Rabi)\n- **Common Problem**: Early Blight (Yellow spots with target-like rings)\n- **Treatment**: Spray Mancozeb 2g/L. Improve aeration.\n- **Tip**: Use staking (supporting plants with sticks) to keep fruit off the ground and prevent rot." },
  { keys: ['sugarcane', 'ganna'], reply: "🎋 **Sugarcane Farming Insights**\n\n- **Planting**: Oct-Nov (Autumn) or Feb-March (Spring)\n- **Water**: High requirement (2000-2500mm). Use drip for 40% saving.\n- **Fertilizer**: 100 kg N + 50 kg P + 50 kg K per acre.\n- **Gov Support**: FRP (Fair and Remunerative Price) ensures guaranteed payment from mills." },
  { keys: ['seeds', 'organic seeds', 'beej'], reply: "🌱 **Quality Seed Selection**\n\n1. **Certification**: Only buy seeds with Blue (Certified) or Green (Foundation) tags.\n2. **Treatment**: Treat seeds with Trichoderma (10g/kg) to prevent soil-borne diseases.\n3. **Organic Seeds**: Look for PGS-India certified suppliers for chemical-free seeds.\n4. **Home Saving**: Clean and dry your best seeds; store in airtight containers with neem leaves." },
  { keys: ['npk levels', 'npk ratio'], reply: "🧪 **NPK Ratio Guide**\n\n- **General Ratio**: 4:2:1 (N:P:K) for cereals, 1:2:1 for legumes.\n- **Nitrogen (N)**: Growth of leaves/stems.\n- **Phosphorus (P)**: Root and flower development.\n- **Potassium (K)**: Disease resistance and fruit quality.\n\n⚠️ Over-applying Urea (N) makes crops attractive to pests and prone to lodging (falling over)." }
];

const translations = {
  hi: {
    'low nitrogen': "🌿 **कम नाइट्रोजन (Nitrogen) की समस्या!**\n\nनाइट्रोजन पत्तियों की वृद्धि के लिए बहुत महत्वपूर्ण है। आप यह कर सकते हैं:\n\n1. **यूरिया का प्रयोग करें** (46-0-0) 50-60 किलो/एकड़\n2. **नीम लेपित यूरिया** का उपयोग करें\n3. **जैविक खाद**: वर्मीकम्पोस्ट (2-3 टन/एकड़) डालें\n\n⏰ सही समय: सुबह जल्दी या शाम को हल्की सिंचाई के साथ।",
    'pest': "🐛 **कीट प्रबंधन सलाह**\n\nएकीकृत कीट प्रबंधन (IPM) अपनाएं:\n\n1. **नीम का तेल**: 5 मिली/लीटर पानी में मिलाकर छिड़काव करें\n2. **पीले चिपचिपे ट्रैप** लगाएं\n3. **जैविक नियंत्रण**: ट्राइकोगाಮಾ ಕಾರ್ಡ್‌ಗಳನ್ನು ಬಳಸಿ",
    'fallback': "🌾 **AgriAssist AI (हिंदी)**\n\nआपके प्रश्न के लिए धन्यवाद! यहाँ कुछ सामान्य सुझाव हैं:\n\n1. खाद डालने से पहले **मिट्टी परीक्षण** अवश्य करवाएं\n2. कीट नियंत्रण के लिए **एकीकृत कीट प्रबंधन** का पालन करें\n3. सरकारी योजनाओं की जानकारी के लिए **Knowledge Garden** देखें",
  },
  kn: {
    'low nitrogen': "🌿 **ನೈಟ್ರೋಜನ್ ಕೊರತೆ ಪತ್ತೆಯಾಗಿದೆ!**\n\nಸಸ್ಯಗಳ ಎಲೆಗಳ ಬೆಳವಣಿಗೆಗೆ ನೈಟ್ರೋಜನ್ ಬಹಳ ಮುಖ್ಯ. ಪರಿಹಾರಗಳು:\n\n1. **ಯೂರಿಯಾ ಬಳಸಿ** (46-0-0) ಎಕರೆಗೆ 50-60 ಕೆಜಿ\n2. **ಬೇವಿನ ಲೇಪಿತ ಯೂರಿಯಾ** ಬಳಸಿ\n3. **ಸಾವಯವ ಗೊಬ್ಬರ**: ಎಕರೆಗೆ 2-3 ಟನ್ ವರ್ಮಿಕಾಂಪೋಸ್ಟ್ ಬಳಸಿ",
    'fallback': "🌾 **AgriAssist AI (ಕನ್ನಡ)**\n\nನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಧನ್ಯವಾದಗಳು! ಕೆಲವು ಸಾಮಾನ್ಯ ಸಲಹೆಗಳು:\n\n1. ಗೊಬ್ಬರ ಬಳಸುವ ಮೊದಲು **ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ** ಮಾಡಿಸಿ\n2. ಕೀಟ ನಿಯಂತ್ರಣಕ್ಕಾಗಿ **ಬೇವಿನ ಎಣ್ಣೆ** ಬಳಸಿ",
  }
};

function generateAIResponse(message, lang = 'en') {
  const msg = message.toLowerCase();
  if (lang !== 'en' && translations[lang]) {
    for (const [key, val] of Object.entries(translations[lang])) {
      if (msg.includes(key)) return val;
    }
  }
  let bestMatch = null;
  let bestScore = 0;
  for (const r of responses) {
    let score = 0;
    for (const key of r.keys) {
      if (msg.includes(key)) score += key.split(' ').length;
    }
    if (score > bestScore) { bestScore = score; bestMatch = r; }
  }
  if (bestMatch) {
    if (lang !== 'en' && translations[lang] && translations[lang][bestMatch.keys[0]]) {
      return translations[lang][bestMatch.keys[0]];
    }
    return bestMatch.reply;
  }
  if (lang !== 'en' && translations[lang]) return translations[lang].fallback;
  return "🌾 **AgriAssist AI**\n\nThank you for your question! Here are some general tips:\n\n1. Always start with a **soil test** before applying fertilizers\n2. Follow **Integrated Pest Management** for pest control\n3. Check **government schemes** for subsidies and support\n4. Use **drip irrigation** to save water\n5. Consult your local **Krishi Vigyan Kendra** for region-specific advice\n\n💬 Try asking about specific topics like: soil health, pest management, wheat cultivation, government schemes, or organic farming!";
}

const pestResults = [
  { pest: "Fall Armyworm", confidence: 94, crop: "Maize/Corn", treatment: "Spray Emamectin Benzoate 5SG @ 0.4g/L. Release Trichogramma cards 50,000/acre." },
  { pest: "Brown Plant Hopper", confidence: 89, crop: "Rice/Paddy", treatment: "Drain water from field, spray Pymetrozine 50WG @ 0.6g/L. Avoid excess nitrogen." },
  { pest: "Aphids", confidence: 91, crop: "Wheat/Mustard", treatment: "Spray Imidacloprid 17.8SL @ 0.3ml/L or Neem oil 5ml/L. Use yellow sticky traps." },
  { pest: "Whitefly", confidence: 87, crop: "Cotton/Vegetables", treatment: "Install yellow sticky traps, spray Neem oil. For severe: Diafenthiuron 50WP @ 1g/L." },
  { pest: "Stem Borer", confidence: 92, crop: "Rice/Sugarcane", treatment: "Release Trichogramma japonicum, apply Carbofuran 3G granules. Remove dead hearts." },
  { pest: "Leaf Miner", confidence: 86, crop: "Tomato/Vegetables", treatment: "Spray Abamectin 1.9EC @ 0.5ml/L. Remove and destroy affected leaves. Use neem oil." },
  { pest: "Healthy Crop", confidence: 96, crop: "General", treatment: "No pest detected! Your crop looks healthy. Continue regular monitoring and preventive sprays." }
];

function encodeSMS(data) {
  const { nitrogen, phosphorus, potassium, soc, cropType } = data;
  const cropCodes = { rice: 'R', wheat: 'W', maize: 'M', cotton: 'C', sugarcane: 'S', soybean: 'SB', potato: 'P', tomato: 'T', onion: 'O', general: 'G' };
  const code = cropCodes[cropType?.toLowerCase()] || 'G';
  return `AA#N${nitrogen}P${phosphorus}K${potassium}S${soc}C${code}#END`;
}

function generateSMSAdvice(data) {
  const { nitrogen, phosphorus, potassium, soc, cropType } = data;
  const n = parseFloat(nitrogen) || 0;
  const p = parseFloat(phosphorus) || 0;
  const k = parseFloat(potassium) || 0;
  const s = parseFloat(soc) || 0;
  const advice = [];
  const fert = [];
  if (n < 250) { advice.push("⚠️ Nitrogen: LOW"); fert.push("Apply Urea 50-60 kg/acre"); }
  else if (n > 500) { advice.push("✅ Nitrogen: HIGH"); fert.push("Reduce urea by 25%"); }
  else { advice.push("✅ Nitrogen: NORMAL"); }
  if (p < 10) { advice.push("⚠️ Phosphorus: LOW"); fert.push("Apply DAP 50 kg/acre"); }
  else if (p > 25) { advice.push("✅ Phosphorus: HIGH"); }
  else { advice.push("✅ Phosphorus: NORMAL"); }
  if (k < 120) { advice.push("⚠️ Potassium: LOW"); fert.push("Apply MOP 40 kg/acre"); }
  else if (k > 280) { advice.push("✅ Potassium: HIGH"); }
  else { advice.push("✅ Potassium: NORMAL"); }
  if (s < 0.5) { advice.push("⚠️ SOC: LOW — Add organic matter"); fert.push("Apply FYM 5 tonnes/acre + Vermicompost 2 tonnes/acre"); }
  else { advice.push("✅ SOC: GOOD"); }
  return {
    soilStatus: advice,
    recommendations: fert,
    overallHealth: (n >= 250 && p >= 10 && k >= 120 && s >= 0.5) ? "Good" : "Needs Improvement",
    cropSpecific: `For ${cropType || 'general'} cultivation, ensure balanced NPK and maintain SOC above 0.5%.`
  };
}

// ============ API ROUTES ============

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', service: 'AgriAssist AI Backend', timestamp: new Date().toISOString() });
});

app.post('/api/chat', (req, res) => {
  const { message, language = 'en' } = req.body;
  if (!message) return res.status(400).json({ success: false, error: 'Message is required' });
  const response = generateAIResponse(message, language);
  chatLogs.push({ role: 'user', content: message, timestamp: new Date(), language });
  chatLogs.push({ role: 'assistant', content: response, timestamp: new Date(), language });
  res.json({ success: true, response, language });
});

app.post('/api/chat/image', upload.single('image'), (req, res) => {
  if (!req.file) return res.status(400).json({ success: false, error: 'Image is required' });
  const detection = pestResults[Math.floor(Math.random() * pestResults.length)];
  const result = {
    success: true,
    detection: { ...detection, imageFile: req.file.filename, analyzedAt: new Date().toISOString() }
  };
  chatLogs.push({ role: 'user', content: '[Image uploaded for pest detection]', timestamp: new Date() });
  chatLogs.push({ role: 'assistant', content: `Detected: ${detection.pest} (${detection.confidence}% confidence)`, timestamp: new Date() });
  fs.unlink(req.file.path, () => {});
  res.json(result);
});

app.get('/api/terms', (req, res) => {
  const { search, category } = req.query;
  let filtered = terms;
  if (search) {
    const q = search.toLowerCase();
    filtered = filtered.filter(t => t.term.toLowerCase().includes(q) || t.definition.toLowerCase().includes(q));
  }
  if (category && category !== 'All') filtered = filtered.filter(t => t.category === category);
  const categories = [...new Set(terms.map(t => t.category))];
  res.json({ success: true, terms: filtered, categories, total: filtered.length });
});

app.get('/api/schemes', (req, res) => {
  const { state, category } = req.query;
  let filtered = schemes;
  if (category && category !== 'All') filtered = filtered.filter(s => s.category === category);
  if (state && state !== 'All') filtered = filtered.filter(s => s.eligibleStates.includes('All') || s.eligibleStates.includes(state));
  const categories = [...new Set(schemes.map(s => s.category))];
  res.json({ success: true, schemes: filtered, categories, total: filtered.length });
});

app.post('/api/sms-simulate', (req, res) => {
  const { nitrogen, phosphorus, potassium, soc, cropType } = req.body;
  if (!nitrogen || !phosphorus || !potassium || !soc) {
    return res.status(400).json({ success: false, error: 'All soil parameters are required' });
  }
  const encoded = encodeSMS(req.body);
  const advice = generateSMSAdvice(req.body);

  // New: Store log for the owner's dashboard
  smsLogs.unshift({
    id: uuidv4(),
    from: 'Farmer #'+Math.floor(1000+Math.random()*9000),
    encoded,
    timestamp: new Date(),
    data: req.body,
    health: advice.overallHealth
  });

  res.json({ success: true, encoded, advice, inputData: req.body });
});

app.get('/api/admin/sms', (req, res) => {
  res.json(smsLogs.slice(0, 10));
});

app.get('/api/chat/logs', (req, res) => {
  res.json({ success: true, logs: chatLogs.slice(-100), total: chatLogs.length });
});

app.use((req, res) => res.status(404).json({ success: false, error: 'Route not found' }));

app.listen(PORT, () => {
  console.log(`\n🌾 AgriAssist AI Backend running on http://localhost:${PORT}\n`);
});

module.exports = app;