'use client';
import { useState, useRef, useEffect } from 'react';

const exampleQueries = [
  "What is the best fertilizer for Rice?",
  "How to control fall armyworm in Maize?",
  "Tell me about PM-KISAN eligibility.",
  "Symptoms of low nitrogen in soil."
];

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [gallery, setGallery] = useState([]);
  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const saved = localStorage.getItem('agri_chat_history');
    if (saved) setMessages(JSON.parse(saved));
    const savedGallery = localStorage.getItem('agri_pest_gallery');
    if (savedGallery) setGallery(JSON.parse(savedGallery));
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const saveState = (msgs, gal) => {
    localStorage.setItem('agri_chat_history', JSON.stringify(msgs));
    if (gal) localStorage.setItem('agri_pest_gallery', JSON.stringify(gal));
  };

  const handleSend = async (msg = input) => {
    if (!msg.trim()) return;
    const newMsgs = [...messages, { role: 'user', content: msg }];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);
    
    try {
      const lang = localStorage.getItem('agri_lang') || 'en';
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, language: lang }),
      });
      const data = await res.json();
      const finalMsgs = [...newMsgs, { role: 'assistant', content: data.response }];
      setMessages(finalMsgs);
      saveState(finalMsgs);
    } catch {
      setMessages([...newMsgs, { role: 'assistant', content: "⚠️ Connection to AI Advisor failed. Please check your network." }]);
    } finally {
      setLoading(false);
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setScanning(true);
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
      const res = await fetch('/api/chat/image', { method: 'POST', body: formData });
      const data = await res.json();
      setTimeout(() => {
        const newGallery = [data.detection, ...gallery].slice(0, 4);
        setGallery(newGallery);
        const finalMsgs = [...messages, 
          { role: 'user', content: "[Neural Scan initiated]" },
          { role: 'assistant', content: `🔍 **Pest Diagnosis Complete**\n\nDetected: **${data.detection.pest}** (${data.detection.confidence}% confidence)\nCrop: ${data.detection.crop}\n\n**Recommendation:** ${data.detection.treatment}` }
        ];
        setMessages(finalMsgs);
        saveState(finalMsgs, newGallery);
        setScanning(false);
      }, 3000);
    } catch {
      setScanning(false);
      alert('Scanning failed');
    }
  };

  return (
    <div className="max-w-5xl mx-auto h-[calc(100vh-160px)] flex gap-8 animate-fade-in">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col app-card overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex items-center justify-between bg-gray-50/50">
          <div className="flex items-center gap-3">
             <div className="w-10 h-10 rounded-xl bg-[#1a4d2e] flex items-center justify-center text-white text-xl">🤖</div>
             <div>
               <h2 className="text-base font-extrabold text-gray-900">AI Farming Advisor</h2>
               <div className="flex items-center gap-2">
                 <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
                 <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Active Support</span>
               </div>
             </div>
          </div>
          <button onClick={() => { setMessages([]); setGallery([]); localStorage.clear(); }} className="text-[10px] font-bold text-red-500 uppercase tracking-widest hover:bg-red-50 px-3 py-1.5 rounded-lg transition-all">
            Clear History
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-sm mx-auto space-y-6">
              <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center text-3xl mb-2">👋</div>
              <div>
                <h3 className="text-xl font-extrabold text-gray-900">How can I help you today?</h3>
                <p className="text-sm text-gray-500 mt-2">Ask about soil health, pest control, or government schemes.</p>
              </div>
              <div className="grid gap-2 w-full">
                {exampleQueries.map((q, i) => (
                  <button key={i} onClick={() => handleSend(q)} className="text-left p-4 bg-white border border-gray-100 rounded-xl text-xs font-bold text-gray-600 hover:border-[#1a4d2e]/30 hover:bg-gray-50 transition-all">
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${m.role === 'user' ? 'bg-[#1a4d2e] text-white' : 'bg-gray-100 text-gray-800 border border-gray-200'}`}>
                {m.content.split('\n').map((line, j) => (
                  <p key={j} className={line.startsWith('-') || line.startsWith('1.') ? 'ml-2' : 'mb-1'}>
                    {line}
                  </p>
                ))}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
               <div className="bg-gray-100 p-4 rounded-2xl flex gap-1.5">
                  <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" />
                  <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce delay-75" />
                  <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce delay-150" />
               </div>
            </div>
          )}
          
          {scanning && (
            <div className="app-card p-8 bg-[#1a4d2e]/5 border-[#1a4d2e]/20 text-center space-y-6">
               <div className="relative w-24 h-24 mx-auto">
                 <div className="absolute inset-0 border-4 border-[#1a4d2e]/10 rounded-full" />
                 <div className="absolute inset-0 border-4 border-t-[#1a4d2e] rounded-full animate-spin" />
                 <div className="absolute inset-0 flex items-center justify-center text-3xl">🔬</div>
               </div>
               <div>
                 <h4 className="text-lg font-bold text-[#1a4d2e]">Neural Scan in Progress</h4>
                 <p className="text-xs text-gray-500 font-medium mt-1">Analyzing tissue samples and pest patterns...</p>
               </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="p-6 border-t border-gray-100 bg-gray-50/30">
          <div className="flex gap-4">
            <button 
              onClick={() => fileInputRef.current.click()}
              className="w-12 h-12 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-xl hover:bg-gray-50 transition-all shadow-sm"
              title="Upload Image for Scan"
            >
              📷
            </button>
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} accept="image/*" className="hidden" />
            <div className="flex-1 relative">
              <input 
                type="text" value={input} onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
                placeholder="Type your question here..."
                className="w-full h-12 bg-white border border-gray-200 rounded-xl pl-6 pr-12 text-sm font-medium focus:outline-none focus:border-[#1a4d2e] shadow-sm"
              />
              <button 
                onClick={() => handleSend()}
                className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-[#1a4d2e] text-white rounded-lg flex items-center justify-center hover:bg-[#1a4d2e]/90 transition-all"
              >
                ➔
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Side Profile / Gallery */}
      <div className="w-80 hidden lg:flex flex-col gap-6">
        <div className="app-card p-6">
           <h3 className="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2">
             <span className="w-1 h-4 bg-[#1a4d2e] rounded-full" />
             Neural History
           </h3>
           <div className="space-y-4">
             {gallery.length === 0 ? (
               <div className="py-8 text-center text-gray-400 text-[10px] italic">
                 No recent scans. Upload an image to begin.
               </div>
             ) : (
               gallery.map((item, i) => (
                 <div key={i} className="p-4 bg-gray-50 border border-gray-100 rounded-xl space-y-2">
                    <div className="flex justify-between items-start">
                       <span className="text-[10px] font-bold text-[#1a4d2e] uppercase tracking-widest">{item.pest}</span>
                       <span className="text-[9px] font-black text-gray-400">{item.confidence}%</span>
                    </div>
                    <p className="text-[10px] text-gray-500 line-clamp-2 leading-relaxed">{item.treatment}</p>
                 </div>
               ))
             )}
           </div>
        </div>

        <div className="app-card p-6 bg-gray-50/50">
           <h3 className="text-sm font-bold text-gray-900 mb-2">AI Capability</h3>
           <p className="text-[11px] text-gray-500 leading-relaxed">
             Our models are trained on 10,000+ agricultural datasets covering Indian climate zones and soil types.
           </p>
           <div className="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center">
              <span className="text-[9px] font-bold text-gray-400 uppercase">Knowledge Cutoff</span>
              <span className="text-[9px] font-black text-gray-900">MAY 2026</span>
           </div>
        </div>
      </div>
    </div>
  );
}
