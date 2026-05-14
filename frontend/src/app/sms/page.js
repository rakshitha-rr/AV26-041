'use client';
import { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';

const cropTypes = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Potato', 'Tomato', 'Onion', 'General'];

function encodeSMS(data) {
  const { nitrogen, phosphorus, potassium, soc, cropType } = data;
  const cropCodes = { rice: 'R', wheat: 'W', maize: 'M', cotton: 'C', sugarcane: 'S', soybean: 'SB', potato: 'P', tomato: 'T', onion: 'O', general: 'G' };
  const code = cropCodes[cropType?.toLowerCase()] || 'G';
  return `AA#N${nitrogen}P${phosphorus}K${potassium}S${soc}C${code}#END`;
}

export default function SMSPage() {
  const [form, setForm] = useState({ nitrogen: '', phosphorus: '', potassium: '', soc: '', cropType: 'Rice' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); 
  const [isClient, setIsClient] = useState(false);

  useEffect(() => { setIsClient(true); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/sms-simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      setResult(data);
      setStep(2);
      setTimeout(() => setStep(3), 2000);
    } catch {
      alert('Connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-fade-in">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-200 pb-8">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Offline Bridge</h1>
          <p className="text-gray-500 mt-2 font-medium">Smart soil analysis via compressed SMS protocols.</p>
        </div>
        <div className="badge-info lowercase">Active Bridge</div>
      </div>

      <div className="grid lg:grid-cols-2 gap-12 items-start">
        <div className="space-y-8">
          <div className="app-card p-8">
            <h3 className="text-lg font-bold text-gray-900 mb-6">How the Protocol Works</h3>
            <div className="space-y-8">
              {[
                { s: '01', title: 'Data Entry', desc: 'Input soil test results locally into the offline application.' },
                { s: '02', title: 'SMS Encoding', desc: 'Proprietary logic compresses data into a secure SMS string.' },
                { s: '03', title: 'Server Analysis', desc: 'Remote AI analyzes the string and returns recommendations.' },
              ].map((item, i) => (
                <div key={i} className="flex gap-6">
                  <span className="text-xl font-black text-gray-200">{item.s}</span>
                  <div>
                    <p className="font-bold text-gray-900 mb-1">{item.title}</p>
                    <p className="text-sm text-gray-500 leading-relaxed font-medium">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-6 bg-blue-50/50 border border-blue-100 rounded-2xl flex gap-4">
            <span className="text-xl">ℹ️</span>
            <p className="text-xs text-blue-700 font-bold leading-relaxed tracking-tight uppercase">
              Designed for extreme rural environments with limited internet connectivity. 
              Uses GSMA standard messaging protocols.
            </p>
          </div>
        </div>

        {/* Simulator Area */}
        <div className="flex flex-col items-center">
          <div className="w-[340px] bg-white border-[10px] border-gray-100 rounded-[48px] shadow-2xl overflow-hidden h-[680px] flex flex-col relative">
            <div className="h-6 w-32 bg-gray-100 rounded-b-2xl self-center z-10" />
            
            <div className="flex-1 p-6 flex flex-col bg-white">
              <div className="flex items-center gap-3 mb-8">
                 <div className="w-8 h-8 rounded-lg bg-[#1a4d2e] flex items-center justify-center text-white text-xs font-bold">AA</div>
                 <span className="text-xs font-black text-gray-900 uppercase tracking-widest">AgriAssist Offline</span>
              </div>

              <div className="flex-1">
                {step === 1 && (
                  <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in">
                    <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4">Soil Data Input</p>
                    <div className="grid grid-cols-2 gap-4">
                      {['nitrogen', 'phosphorus', 'potassium', 'soc'].map((field) => (
                        <div key={field}>
                          <label className="text-[10px] text-gray-400 font-bold uppercase mb-1 block">{field}</label>
                          <input 
                            type="number" value={form[field]} onChange={e => setForm({...form, [field]: e.target.value})}
                            placeholder="0" className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 focus:outline-none focus:border-[#1a4d2e] font-bold" required />
                        </div>
                      ))}
                    </div>
                    <div>
                      <label className="text-[10px] text-gray-400 font-bold uppercase mb-1 block">Target Crop</label>
                      <select value={form.cropType} onChange={e => setForm({...form, cropType: e.target.value})} className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 focus:outline-none focus:border-[#1a4d2e] font-bold">
                        {cropTypes.map(c => <option key={c} value={c}>{c}</option>)}
                      </select>
                    </div>
                    <div className="flex gap-2 pt-4">
                      <button type="submit" disabled={loading} className="flex-1 btn-primary text-xs uppercase tracking-widest shadow-lg shadow-green-900/10">
                        {loading ? 'Processing...' : 'Generate Advice'}
                      </button>
                      <button type="button" onClick={() => window.open(`sms:+919876543210?body=AgriAssist: ${encodeSMS(form)}`)} className="w-12 btn-secondary flex items-center justify-center p-0 rounded-xl text-xl">
                        📱
                      </button>
                    </div>
                  </form>
                )}

                {step === 2 && (
                  <div className="flex flex-col items-center justify-center h-full py-10 animate-fade-in">
                     <div className="w-12 h-12 border-4 border-green-100 border-t-green-600 rounded-full animate-spin mb-6" />
                     <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Encrypting Data...</p>
                     <p className="text-[9px] font-mono mt-4 text-gray-300 break-all text-center px-4">{result?.encoded}</p>
                  </div>
                )}

                {step === 3 && result && (
                  <div className="space-y-6 animate-fade-in">
                    <div className="flex items-center justify-between">
                       <span className="text-[10px] font-bold text-gray-400 uppercase">Analysis Complete</span>
                       <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase ${result.advice.overallHealth === 'Good' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>{result.advice.overallHealth}</span>
                    </div>

                    <div className="h-44 w-full bg-gray-50 rounded-2xl border border-gray-100 p-2">
                       {isClient && (
                         <ResponsiveContainer width="100%" height="100%">
                           <RadarChart cx="50%" cy="50%" outerRadius="65%" data={[
                             { subject: 'N', A: Math.min(100, (result.inputData.nitrogen / 400) * 100) },
                             { subject: 'P', A: Math.min(100, (result.inputData.phosphorus / 20) * 100) },
                             { subject: 'K', A: Math.min(100, (result.inputData.potassium / 200) * 100) },
                             { subject: 'SOC', A: Math.min(100, (result.inputData.soc / 0.8) * 100) },
                           ]}>
                             <PolarGrid stroke="#e5e7eb" />
                             <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 10, fontWeight: 'bold' }} />
                             <Radar name="Soil" dataKey="A" stroke="#166534" fill="#22c55e" fillOpacity={0.4} />
                           </RadarChart>
                         </ResponsiveContainer>
                       )}
                    </div>

                    <div className="space-y-2">
                       {result.advice.recommendations.map((r, i) => (
                         <div key={i} className="p-3 bg-gray-50 border border-gray-100 rounded-xl flex gap-3 items-center">
                            <span className="w-1.5 h-1.5 bg-green-600 rounded-full" />
                            <p className="text-[10px] font-bold text-gray-700">{r}</p>
                         </div>
                       ))}
                    </div>

                    <button onClick={() => setStep(1)} className="w-full py-3 bg-gray-100 hover:bg-gray-200 text-gray-400 text-[10px] font-bold uppercase rounded-xl tracking-widest transition-all">
                      Reset Simulator
                    </button>
                  </div>
                )}
              </div>

              <div className="h-2 w-24 bg-gray-100 rounded-full self-center mb-4" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
