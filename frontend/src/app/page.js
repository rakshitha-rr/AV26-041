'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useLanguage } from '@/context/LanguageContext';

/**
 * Farmer Dashboard - AgriIntel
 * Main central hub for farmers to manage predictions, risks, and history.
 */
export default function FarmerDashboard() {
  const { t, formatNumber } = useLanguage();
  const [aadhaar, setAadhaar] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [predictLoading, setPredictLoading] = useState(false);
  const [time, setTime] = useState(new Date());
  const router = useRouter();

  // Form State for Yield Prediction
  const [formData, setFormData] = useState({
    rainfall_mm: 750,
    temperature_c: 28,
    soil_ph: 6.5,
    soil_moisture_pct: 45,
    fertilizer_kg_per_hectare: 120,
    irrigation_level_pct: 70
  });

  useEffect(() => {
    const token = localStorage.getItem('agri_token');
    const storedAadhaar = localStorage.getItem('farmer_aadhaar');
    
    if (!token) {
      router.push('/login');
      return;
    }

    setAadhaar(storedAadhaar);
    fetchDashboardData(token);
    
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, [router]);

  const fetchDashboardData = async (token) => {
    const apiHost = window.location.hostname;
    try {
      // 1. Fetch Prediction History
      const histRes = await fetch(`http://${apiHost}:8000/api/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const histData = await histRes.json();
      setHistory(histData.predictions || []);

      // 2. Fetch Initial Risk Alerts (using default/stored values)
      const alertRes = await fetch(`http://${apiHost}:8000/api/risk-alerts`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const alertData = await alertRes.json();
      setAlerts(alertData.alerts || []);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredictLoading(true);
    const token = localStorage.getItem('agri_token');

    const apiHost = window.location.hostname;
    try {
      const res = await fetch(`http://${apiHost}:8000/api/predict-yield`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setPrediction(data);
      
      // Refresh history and alerts
      fetchDashboardData(token);
    } catch (err) {
      alert("Failed to connect to ML Engine.");
    } finally {
      setPredictLoading(false);
    }
  };

  if (loading) return (
    <div className="flex h-screen items-center justify-center">
      <div className="w-12 h-12 border-4 border-[#1a4d2e]/10 border-t-[#1a4d2e] rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fade-in pb-20">
      
      {/* Header Section */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-100 pb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider">{t('farmer_account')}</span>
            <span className="text-gray-300">|</span>
            <span className="text-xs font-bold text-gray-400">{t('id')}: {formatNumber(aadhaar)}</span>
          </div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            {t('welcome')}
          </h1>
          <p className="text-gray-500 mt-2 font-medium">{t('tagline')}</p>
        </div>
        <div className="flex items-center gap-4 text-sm font-bold text-gray-400 uppercase tracking-widest bg-white px-6 py-3 rounded-2xl shadow-sm border border-gray-50">
           <span className="text-gray-900">{formatNumber(time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }))}</span>
           <span className="text-gray-100">|</span>
           <span>{formatNumber(time.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' }))}</span>
        </div>
      </header>

      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Left Column: Yield Prediction & Tool */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Risk Alerts Banner */}
          {alerts.length > 0 && (
            <div className="space-y-4">
               <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">{t('alerts')}</h3>
               <div className="grid gap-4">
                  {alerts.map((alert, idx) => (
                    <div key={idx} className={`p-5 rounded-[1.5rem] border flex items-start gap-5 transition-all hover:scale-[1.01] ${
                      alert.risk_level === 'critical' ? 'bg-red-50 border-red-100' : 'bg-amber-50 border-amber-100'
                    }`}>
                      <div className="text-3xl">{alert.icon}</div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className={`font-bold text-sm ${alert.risk_level === 'critical' ? 'text-red-700' : 'text-amber-700'}`}>
                            {alert.risk_type}
                          </h4>
                          <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded-md ${
                            alert.risk_level === 'critical' ? 'bg-red-100 text-red-600' : 'bg-amber-100 text-amber-600'
                          }`}>
                            {alert.risk_level}
                          </span>
                        </div>
                        <p className="text-gray-700 text-sm font-medium leading-relaxed mb-3">{alert.message}</p>
                        <div className="bg-white/50 p-3 rounded-xl border border-white/20 text-xs font-semibold text-gray-600 italic">
                          💡 {t('suggestion')} {alert.recommendation}
                        </div>
                      </div>
                    </div>
                  ))}
               </div>
            </div>
          )}

          {/* Main Predictor Tool */}
          <section className="bg-white p-8 md:p-10 rounded-[2.5rem] shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-8">
               <div>
                  <h3 className="text-2xl font-bold text-gray-900">{t('yield_predictor')}</h3>
                  <p className="text-sm text-gray-400 font-medium">{t('ml_engine')}</p>
               </div>
               <div className="w-12 h-12 bg-green-50 rounded-2xl flex items-center justify-center text-xl">🚀</div>
            </div>

            <form onSubmit={handlePredict} className="grid md:grid-cols-2 gap-8">
              {Object.keys(formData).map((key) => (
                <div key={key} className="space-y-2">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider ml-1">
                    {t(key.split('_')[0])} {key.includes('mm') ? '(mm)' : key.includes('c') ? '(°C)' : key.includes('pct') ? '(%)' : ''}
                  </label>
                  <input 
                    type="number"
                    step="0.1"
                    className="w-full bg-gray-50 border-none rounded-2xl px-6 py-4 focus:ring-2 focus:ring-[#1a4d2e] transition-all text-gray-800 font-bold"
                    value={formData[key]}
                    onChange={(e) => setFormData({...formData, [key]: parseFloat(e.target.value)})}
                    required
                  />
                </div>
              ))}
              <div className="md:col-span-2 pt-4">
                <button 
                  type="submit"
                  disabled={predictLoading}
                  className="w-full bg-[#1a4d2e] hover:bg-[#2a6d41] text-white font-bold py-5 rounded-2xl shadow-lg shadow-green-900/10 transition-all flex items-center justify-center gap-3 active:scale-[0.98] disabled:opacity-50"
                >
                  {predictLoading ? (
                    <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <>{t('predict')} ✨</>
                  )}
                </button>
              </div>
            </form>

            {/* Result Display */}
            {prediction && (
              <div className="mt-10 p-8 rounded-[2rem] bg-gradient-to-br from-[#1a4d2e] to-[#4f6f52] text-white animate-fade-in shadow-2xl">
                 <div className="flex items-center justify-between mb-6">
                     <span className="text-[10px] font-bold uppercase tracking-[0.2em] opacity-80">{t('ai_analysis')}</span>
                     <span className="bg-white/20 px-3 py-1 rounded-full text-[10px] font-bold uppercase">{t('confidence')}: {formatNumber(prediction.confidence_score)}%</span>
                 </div>
                 <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
                    <div>
                       <h2 className="text-5xl font-black mb-1">{formatNumber(prediction.predicted_yield_tons_per_hectare)} <span className="text-xl opacity-70">{t('tons_per_ha')}</span></h2>
                       <p className="text-lg font-bold opacity-90 uppercase tracking-widest">{prediction.yield_category} {t('yield_performance')}</p>
                    </div>
                    <div className="bg-white/10 backdrop-blur-md px-6 py-4 rounded-2xl border border-white/10 text-center">
                       <p className="text-[10px] font-bold uppercase mb-1">{t('status_rating')}</p>
                       <p className="text-xl font-black tracking-tighter">{(prediction?.yield_category || 'UNKNOWN').replace('_', ' ')}</p>
                    </div>
                 </div>
                 <div className="space-y-4 pt-6 border-t border-white/10">
                    <p className="text-sm font-medium leading-relaxed italic">" {prediction?.interpretation || t('pending_analysis')} "</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                       {prediction?.recommendations?.map((rec, i) => (
                         <div key={i} className="flex items-start gap-3 text-xs bg-white/5 p-3 rounded-xl">
                            <span className="text-lg">✅</span>
                            <span className="font-medium text-white/90">{rec}</span>
                         </div>
                       ))}
                    </div>
                 </div>
              </div>
            )}
          </section>

          {/* Quick Support Sidebar (Horizontal on Small, Grid on Large) */}
          <div className="grid md:grid-cols-2 gap-6">
             <Link href="/chatbot" className="app-card p-8 bg-[#1a4d2e]/5 border-[#1a4d2e]/10 group hover:bg-[#1a4d2e]/10 transition-all">
                <div className="text-3xl mb-4 group-hover:scale-110 transition-transform">🤖</div>
                <h4 className="text-lg font-bold text-gray-900 mb-1">{t('farming_assistant')}</h4>
                <p className="text-xs text-gray-500 font-medium">{t('farming_assistant_desc')}</p>
             </Link>
             <Link href="/knowledge" className="app-card p-8 bg-gray-50 border-gray-100 group hover:border-[#1a4d2e]/20 transition-all">
                <div className="text-3xl mb-4 group-hover:scale-110 transition-transform">🌱</div>
                <h4 className="text-lg font-bold text-gray-900 mb-1">{t('knowledge')}</h4>
                <p className="text-xs text-gray-500 font-medium">{t('explore_terms')}</p>
             </Link>
          </div>
        </div>

        {/* Right Column: History & Trends */}
        <div className="space-y-8">
          
          {/* Market Glance */}
          <div className="app-card p-8">
             <h3 className="text-sm font-bold text-gray-900 mb-6 flex items-center gap-2 uppercase tracking-widest opacity-40">
                {t('market_trends')}
             </h3>
             <div className="space-y-6">
                {[
                  { crop: 'Wheat', price: `₹${formatNumber('2,350')}`, trend: `+${formatNumber('1.5')}%`, up: true },
                  { crop: 'Ragi', price: `₹${formatNumber('3,840')}`, trend: `+${formatNumber('0.8')}%`, up: true },
                  { crop: 'Maize', price: `₹${formatNumber('1,960')}`, trend: `-${formatNumber('0.3')}%`, up: false }
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl">
                     <div>
                        <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{t(item.crop.toLowerCase())}</p>
                        <p className="text-lg font-black text-gray-900">{item.price}</p>
                     </div>
                     <span className={`text-[10px] font-black px-2 py-1 rounded-lg ${item.up ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                        {item.up ? '▲' : '▼'} {item.trend}
                     </span>
                  </div>
                ))}
             </div>
          </div>

          {/* Prediction History Timeline */}
          <div className="app-card p-8 bg-white overflow-hidden">
             <div className="flex items-center justify-between mb-8">
                <h3 className="text-sm font-bold text-gray-900 uppercase tracking-widest opacity-40">{t('history')}</h3>
                <span className="text-[10px] font-bold text-[#1a4d2e]">{formatNumber(history.length)} {t('reports')}</span>
             </div>
             <div className="space-y-8 relative before:absolute before:inset-0 before:left-3 before:w-0.5 before:bg-gray-100 before:h-full">
                {history.length === 0 ? (
                  <p className="text-xs text-gray-400 italic text-center py-10">{t('no_reports')}</p>
                ) : (
                  history.map((item, idx) => (
                    <div key={idx} className="relative pl-10">
                       <div className="absolute left-0 top-1 w-6 h-6 rounded-full bg-white border-4 border-[#1a4d2e] z-10" />
                       <div className="space-y-1">
                          <p className="text-[10px] font-bold text-gray-400 uppercase">{new Date(item.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}</p>
                          <p className="text-sm font-bold text-gray-900">{formatNumber(item.predicted_yield)} {t('tons_per_ha')}</p>
                          <p className="text-[10px] font-black text-[#1a4d2e] uppercase tracking-wider">{item.yield_rating.replace('_', ' ')}</p>
                       </div>
                    </div>
                  ))
                )}
             </div>
          </div>

          {/* Featured Scheme */}
          <div className="bg-[#1a4d2e] p-8 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden">
             <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
             <h4 className="text-xs font-bold uppercase tracking-[0.2em] mb-4 opacity-70">{t('top_scheme')}</h4>
             <h3 className="text-2xl font-black mb-3 leading-tight">{t('pm_kisan_nidhi')}</h3>
             <p className="text-sm font-medium text-white/80 leading-relaxed mb-8">{t('pm_kisan_desc')}</p>
             <Link href="/knowledge" className="inline-flex items-center gap-2 bg-white text-[#1a4d2e] px-6 py-3 rounded-xl font-bold text-xs hover:bg-gray-100 transition-all active:scale-[0.98]">
                {t('apply_now')}
             </Link>
          </div>
        </div>

      </div>
    </div>
  );
}
