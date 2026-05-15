'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { useLanguage } from '@/context/LanguageContext';

/**
 * AgriIntel Login Page
 * Features Aadhaar-based authentication with a premium glassmorphism design.
 */
export default function LoginPage() {
  const [aadhaar, setAadhaar] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const { language, switchLanguage, t } = useLanguage();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Remove spaces from Aadhaar for backend validation
    const cleanAadhaar = aadhaar.replace(/\s/g, '');
    
    if (cleanAadhaar.length !== 12) {
      setError(t('valid_aadhaar_error'));
      setLoading(false);
      return;
    }

    try {
      const apiHost = window.location.hostname;
      const response = await fetch(`http://${apiHost}:8000/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          aadhaar_number: cleanAadhaar,
          phone_number: phone
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Store session data
        localStorage.setItem('agri_token', data.session_token);
        localStorage.setItem('farmer_aadhaar', cleanAadhaar);
        localStorage.setItem('farmer_phone', phone);
        
        // Redirect to main dashboard
        router.push('/');
      } else {
        setError(data.message || t('login_failed'));
      }
    } catch (err) {
      setError(t('connection_failed'));
    } finally {
      setLoading(false);
    }
  };

  const formatAadhaar = (val) => {
    const v = val.replace(/\D/g, '').slice(0, 12);
    const m = v.match(/.{1,4}/g);
    return m ? m.join(' ') : v;
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#0a1a0f]">
      {/* Dynamic Background Image */}
      <div className="absolute inset-0 z-0 opacity-40 scale-105 animate-slow-zoom">
        <Image 
          src="/login_bg.png" 
          alt="Karnataka Farm" 
          fill
          className="object-cover"
          priority
        />
      </div>

      {/* Decorative Overlays */}
      <div className="absolute inset-0 z-1 bg-gradient-to-tr from-[#0a1a0f] via-transparent to-transparent opacity-80"></div>

      {/* Login Container */}
      <div className="relative z-10 w-full max-w-md px-6 animate-fade-in">
        <div className="bg-white/95 backdrop-blur-2xl p-8 md:p-10 rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.3)] border border-white/20">
          
          <div className="text-center mb-10">
            <div className="flex justify-center gap-2 mb-8">
              {['en', 'kn', 'hi'].map(l => (
                <button 
                  key={l}
                  onClick={() => switchLanguage(l)}
                  className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase transition-all ${language === l ? 'bg-[#1a4d2e] text-white' : 'bg-gray-100 text-gray-400 hover:bg-gray-200'}`}
                >
                  {l}
                </button>
              ))}
            </div>
            <div className="inline-flex items-center justify-center w-20 h-20 bg-[#1a4d2e]/10 rounded-3xl mb-4">
               <span className="text-4xl">🌾</span>
            </div>
            <h1 className="text-4xl font-extrabold text-[#1a4d2e] mb-2 tracking-tight">{t('login_title')}</h1>
            <p className="text-gray-500 font-medium">{t('login_subtitle')}</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="group">
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 ml-1 transition-colors group-focus-within:text-[#1a4d2e]">
                {t('aadhaar_label')}
              </label>
              <input 
                type="text"
                placeholder="0000 0000 0000"
                className="w-full px-6 py-4 rounded-2xl bg-gray-50 border border-gray-100 focus:bg-white focus:ring-2 focus:ring-[#1a4d2e] focus:border-transparent outline-none transition-all text-xl tracking-[0.2em] font-mono text-gray-800"
                value={aadhaar}
                onChange={(e) => setAadhaar(formatAadhaar(e.target.value))}
                required
              />
            </div>

            <div className="group">
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 ml-1 transition-colors group-focus-within:text-[#1a4d2e]">
                {t('phone_label')}
              </label>
              <input 
                type="tel"
                placeholder="+91 00000 00000"
                className="w-full px-6 py-4 rounded-2xl bg-gray-50 border border-gray-100 focus:bg-white focus:ring-2 focus:ring-[#1a4d2e] focus:border-transparent outline-none transition-all text-xl text-gray-800"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 text-red-600 p-4 rounded-2xl text-sm font-semibold border border-red-100 flex items-center gap-3 animate-bounce-short">
                <span className="text-lg">⚠️</span>
                {error}
              </div>
            )}

            <button 
              type="submit"
              disabled={loading}
              className="w-full bg-[#1a4d2e] hover:bg-[#2a6d41] text-white font-bold py-5 rounded-2xl shadow-xl shadow-green-900/30 transition-all hover:translate-y-[-2px] active:scale-[0.98] disabled:opacity-70 flex items-center justify-center gap-3 text-lg"
            >
              {loading ? (
                <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>{t('login_button')}</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </>
              )}
            </button>
          </form>

        </div>
        
        <p className="text-center text-white/50 mt-10 text-[10px] font-bold uppercase tracking-[0.3em]">
          {t('certified_system')}
        </p>
      </div>

      <style jsx global>{`
        @keyframes slow-zoom {
          0% { transform: scale(1.05); }
          50% { transform: scale(1.1); }
          100% { transform: scale(1.05); }
        }
        .animate-slow-zoom {
          animation: slow-zoom 20s infinite ease-in-out;
        }
        @keyframes bounce-short {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-4px); }
        }
        .animate-bounce-short {
          animation: bounce-short 0.3s ease-in-out;
        }
      `}</style>
    </div>
  );
}
