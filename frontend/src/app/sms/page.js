'use client';

import { useState } from 'react';
import { useLanguage } from '@/context/LanguageContext';

/**
 * Offline Bridge - SMS & Voice Support
 * Provides farmers with ways to connect when internet is unavailable.
 */
export default function OfflineBridgePage() {
  const [formData, setFormData] = useState({
    rainfall: 750,
    temp: 28,
    ph: 6.5,
    moisture: 45,
    fertilizer: 120,
    irrigation: 70
  });
  
  const { t, formatNumber } = useLanguage();

  // Updated to include +91 country code for proper Indian network routing
  const supportNumber = "+919916721196";

  const generateSMS = () => {
    return `YIELD ${formData.rainfall} ${formData.temp} ${formData.ph} ${formData.moisture} ${formData.fertilizer} ${formData.irrigation}`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generateSMS());
    alert(t('sms_copied'));
  };

  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-fade-in pb-20">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-100 pb-8">
        <div>
          <h1 className="text-4xl font-black text-gray-900 tracking-tight">{t('sms_bridge')}</h1>
          <p className="text-gray-500 mt-2 font-medium">{t('sms_desc')}</p>
        </div>
        <div className="bg-amber-50 text-amber-700 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border border-amber-100">
          {t('emergency_mode')}
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-10">
        
        {/* Left Column: Call Support */}
        <div className="space-y-8">
          <div className="bg-gradient-to-br from-[#1a4d2e] to-[#2a6d41] p-10 rounded-[3rem] text-white shadow-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 group-hover:scale-110 transition-transform" />
            <h3 className="text-sm font-bold uppercase tracking-[0.2em] mb-6 opacity-80">{t('voice_support')}</h3>
            <h2 className="text-4xl font-black mb-4">{t('talk_expert')}</h2>
            <p className="text-white/70 text-sm font-medium mb-10 leading-relaxed max-w-xs">
              {t('call_desc')}
            </p>
            
            <a 
              href={`tel:${supportNumber}`}
              className="inline-flex items-center gap-4 bg-white text-[#1a4d2e] px-8 py-5 rounded-[2rem] font-black text-xl hover:bg-gray-100 transition-all active:scale-[0.95] shadow-xl shadow-black/20"
            >
              <span>📞</span> {formatNumber(supportNumber)}
            </a>
          </div>


        </div>

        {/* Right Column: SMS Builder */}
        <div className="app-card p-10 space-y-8 bg-white border-none shadow-xl">
           <div>
              <h3 className="text-2xl font-black text-gray-900">{t('sms_builder')}</h3>
              <p className="text-sm text-gray-400 font-medium">{t('sms_builder_desc')}</p>
           </div>

           <div className="grid grid-cols-2 gap-6">
              {Object.keys(formData).map((key) => (
                <div key={key} className="space-y-2">
                  <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">{t(key)}</label>
                  <input 
                    type="number"
                    value={formData[key]}
                    onChange={(e) => setFormData({...formData, [key]: e.target.value})}
                    className="w-full bg-gray-50 border-none rounded-2xl px-5 py-4 text-sm font-bold text-gray-800 focus:ring-2 focus:ring-[#1a4d2e] transition-all"
                  />
                </div>
              ))}
           </div>

           <div className="space-y-4 pt-6">
              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">{t('generated_string')}</p>
              <div className="bg-gray-900 p-6 rounded-[2rem] text-green-400 font-mono text-lg break-all flex items-center justify-between gap-4 border-4 border-gray-800">
                 <span className="tracking-tighter">{generateSMS()}</span>
                 <button onClick={handleCopy} className="bg-white/10 hover:bg-white/20 p-3 rounded-xl transition-all" title="Copy to Clipboard">
                    📋
                 </button>
              </div>
           </div>

           <div className="pt-6">
              <a 
                href={`sms:${supportNumber}?body=${encodeURIComponent(generateSMS())}`}
                className="w-full bg-[#1a4d2e] hover:bg-[#2a6d41] text-white font-black py-5 rounded-[2rem] shadow-lg shadow-green-900/10 transition-all flex items-center justify-center gap-3 active:scale-[0.98]"
              >
                {t('send_sms')}
              </a>
           </div>

           <div className="p-6 bg-amber-50 rounded-2xl border border-amber-100 flex gap-4">
              <div className="text-xl">💡</div>
              <p className="text-xs text-amber-800 font-medium leading-relaxed">
                {t('sms_tip')}
              </p>
           </div>
        </div>

      </div>
    </div>
  );
}
