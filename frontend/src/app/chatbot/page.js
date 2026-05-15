'use client';

import { useState, useRef, useEffect } from 'react';
import { useLanguage } from '@/context/LanguageContext';

/**
 * Farming Advisor - Multilingual Voice AI Agent
 * Supports EN, HI, KN with Speech-to-Text and Text-to-Speech.
 */
export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const { language: lang, switchLanguage, t } = useLanguage();
  const chatEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  useEffect(() => {
    const savedMsgs = localStorage.getItem('agri_chat_history');
    if (savedMsgs) setMessages(JSON.parse(savedMsgs));
    
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const saveState = (msgs) => {
    localStorage.setItem('agri_chat_history', JSON.stringify(msgs));
  };

  // ─── Text Chat ───────────────────────────────────────────────
  const handleSend = async (msg = input) => {
    if (!msg.trim()) return;
    const userMsg = { role: 'user', content: msg, type: 'text' };
    const newMsgs = [...messages, userMsg];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);
    
    const apiHost = window.location.hostname;
    try {
      const res = await fetch(`http://${apiHost}:8000/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: msg, language: lang }),
      });
      const data = await res.json();
      const assistantMsg = { role: 'assistant', content: data.response, type: 'text' };
      const finalMsgs = [...newMsgs, assistantMsg];
      setMessages(finalMsgs);
      saveState(finalMsgs);
    } catch {
      setMessages([...newMsgs, { role: 'assistant', content: "⚠️ Connection failed.", type: 'text' }]);
    } finally {
      setLoading(false);
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // ─── Voice AI ───────────────────────────────────────────────
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' });
        sendVoiceQuery(audioBlob);
      };
      mediaRecorderRef.current.start();
      setRecording(true);
    } catch {
      alert("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      mediaRecorderRef.current.stream.getTracks().forEach(t => t.stop());
    }
  };

  const sendVoiceQuery = async (blob) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('audio', blob, 'query.wav');
    formData.append('language', lang);

    const tempMsgs = [...messages, { role: 'user', content: "🎤 [Voice Query]", type: 'voice' }];
    setMessages(tempMsgs);

    const apiHost = window.location.hostname;
    try {
      const res = await fetch(`http://${apiHost}:8000/api/voice/voice-assistant`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      
      const assistantMsg = { 
        role: 'assistant', 
        content: data.text_response, 
        audio: `http://${apiHost}:8000${data.audio_url}`,
        type: 'voice' 
      };
      
      const finalMsgs = [...tempMsgs, assistantMsg];
      setMessages(finalMsgs);
      saveState(finalMsgs);
      
      // Auto-play response
      const audio = new Audio(`http://${apiHost}:8000${data.audio_url}`);
      audio.play();
    } catch {
      setMessages([...tempMsgs, { role: 'assistant', content: "⚠️ Voice failed.", type: 'text' }]);
    } finally {
      setLoading(false);
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[85vh] flex flex-col bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border border-gray-100">
      
      {/* Header */}
      <div className="bg-[#1a4d2e] p-6 text-white flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center text-2xl">🤖</div>
          <div>
            <h1 className="font-black text-lg tracking-tight">{t('chatbot_title')}</h1>
            <p className="text-xs text-white/60 font-bold uppercase tracking-widest">{t('chatbot_subtitle')}</p>
          </div>
        </div>
        
        {/* Language Switcher */}
        <div className="flex bg-white/10 p-1 rounded-xl border border-white/10">
          {['en', 'kn', 'hi'].map((l) => (
            <button 
              key={l}
              onClick={() => switchLanguage(l)}
              className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase transition-all ${lang === l ? 'bg-white text-[#1a4d2e]' : 'text-white/60 hover:text-white'}`}
            >
              {l}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/50">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-40">
            <span className="text-6xl mb-4">🌾</span>
            <h3 className="text-xl font-bold text-gray-900">{t('how_can_help')}</h3>
            <p className="text-xs font-medium max-w-xs mt-2">{t('ask_me')}</p>
          </div>
        )}
        
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
            <div className={`max-w-[80%] p-5 rounded-[1.5rem] shadow-sm ${m.role === 'user' ? 'bg-[#1a4d2e] text-white rounded-tr-none' : 'bg-white text-gray-800 rounded-tl-none border border-gray-100'}`}>
              <p className="text-sm font-medium leading-relaxed">{m.content}</p>
              {m.audio && (
                <button onClick={() => new Audio(m.audio).play()} className="mt-3 flex items-center gap-2 text-[10px] font-black uppercase bg-gray-100 px-3 py-1.5 rounded-lg text-[#1a4d2e]">
                  <span>🔊</span> {t('replay_voice')}
                </button>
              )}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 bg-white border-t border-gray-100">
        <div className="flex items-center gap-4">
          <button 
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl transition-all shadow-lg ${recording ? 'bg-red-500 text-white animate-pulse scale-110' : 'bg-gray-100 text-gray-400 hover:bg-gray-200'}`}
          >
            {recording ? '⏹️' : '🎤'}
          </button>
          
          <div className="flex-1 relative">
            <input 
              type="text" value={input} onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder={t('type_question')}
              className="w-full bg-gray-100 border-none rounded-2xl px-6 py-4 text-sm font-medium focus:ring-2 focus:ring-[#1a4d2e] transition-all"
            />
            <button onClick={() => handleSend()} className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-[#1a4d2e] text-white rounded-xl flex items-center justify-center shadow-lg">
              ➔
            </button>
          </div>
        </div>
        
        {recording && (
          <div className="mt-4 flex items-center justify-center gap-2 animate-fade-in">
            <div className="flex gap-1">
              {[1,2,3,4].map(i => <div key={i} className="w-1 h-4 bg-red-400 rounded-full animate-bounce" style={{animationDelay: `${i*0.1}s`}} />)}
            </div>
            <span className="text-[10px] font-black text-red-500 uppercase tracking-widest">{t('listening')}</span>
          </div>
        )}
      </div>
    </div>
  );
}
