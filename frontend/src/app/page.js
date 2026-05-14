'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';

const stats = [
  { label: 'Resources', value: '32 Items', icon: '📖', color: 'text-green-600' },
  { label: 'Active Schemes', value: '12 Available', icon: '🏛️', color: 'text-blue-600' },
  { label: 'Market Trends', value: '+5.4%', icon: '📈', color: 'text-emerald-600' },
  { label: 'Support Coverage', value: 'National', icon: '🌐', color: 'text-gray-600' },
];

export default function HomePage() {
  const [health, setHealth] = useState(null);
  const [time, setTime] = useState(null);
  const [smsLogs, setSmsLogs] = useState([]);

  useEffect(() => {
    fetch('/api/health').then(r => r.ok ? r.json() : null).then(setHealth).catch(() => {});
    const timer = setInterval(() => setTime(new Date()), 1000);
    const fetchSms = () => fetch('/api/admin/sms').then(r => r.ok ? r.json() : []).then(d => { if(Array.isArray(d)) setSmsLogs(d); }).catch(() => {});
    fetchSms();
    const smsTimer = setInterval(fetchSms, 5000);
    return () => { clearInterval(timer); clearInterval(smsTimer); };
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-fade-in">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-200 pb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="badge-success lowercase">v1.0 stable</span>
            {health && <span className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">• Online</span>}
          </div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Farm Dashboard</h1>
          <p className="text-gray-500 mt-2 font-medium">Welcome back. Here is a summary of your farm activities.</p>
        </div>
        <div className="flex items-center gap-4 text-sm font-bold text-gray-400 uppercase tracking-widest">
           <span>{time?.toLocaleDateString([], { month: 'long', day: 'numeric' })}</span>
           <span className="text-gray-200">|</span>
           <span className="text-gray-900">{time?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((s, i) => (
          <div key={i} className="app-card p-6">
            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">{s.label}</p>
            <div className="flex items-center justify-between">
              <span className="text-2xl font-extrabold text-gray-900">{s.value}</span>
              <span className="text-xl">{s.icon}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          <div className="grid md:grid-cols-2 gap-6">
            {[
              { title: 'Farming Advisor', desc: 'AI-driven insights for soil, pests, and crops.', icon: '🤖', href: '/chatbot' },
              { title: 'Knowledge Base', desc: 'Comprehensive guide to schemes and terms.', icon: '📚', href: '/knowledge' },
            ].map((item, i) => (
              <Link key={i} href={item.href} className="app-card p-8 group hover:border-[#1a4d2e]/30">
                <div className="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center text-2xl mb-6 group-hover:bg-[#1a4d2e]/5 transition-colors">
                  {item.icon}
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{item.desc}</p>
              </Link>
            ))}
          </div>

          {/* Admin Feed Section */}
          <div className="app-card p-8 bg-gray-50/50">
            <div className="flex items-center justify-between mb-8">
               <h3 className="text-lg font-bold text-gray-900">Live Activity Feed</h3>
               <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Incoming SMS Data</span>
            </div>
            <div className="space-y-4">
              {smsLogs.length === 0 ? (
                <div className="py-12 text-center text-gray-400 text-sm italic">
                  Waiting for incoming farmer reports...
                </div>
              ) : (
                smsLogs.map((log) => (
                  <div key={log.id} className="flex items-center justify-between p-4 bg-white border border-gray-100 rounded-xl shadow-sm">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-600">
                        {log.from?.includes('#') ? log.from.split('#')[1][0] : 'F'}
                      </div>
                      <div>
                        <p className="text-sm font-bold text-gray-900">{log.from}</p>
                        <p className="text-[10px] text-gray-400 font-mono tracking-tighter">{log.encoded}</p>
                      </div>
                    </div>
                    <div className="text-right flex flex-col items-end gap-1">
                       <span className={`px-2 py-0.5 rounded-md text-[9px] font-black uppercase ${log.health === 'Good' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                         {log.health}
                       </span>
                       <span className="text-[9px] text-gray-400 font-bold uppercase">{new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <div className="app-card p-6">
            <h3 className="text-sm font-bold text-gray-900 mb-6 flex items-center gap-2">
              <span className="w-1 h-4 bg-[#1a4d2e] rounded-full" />
              Mandi Market Trends
            </h3>
            <div className="space-y-5">
              {[
                { label: 'Wheat (Grade A)', price: '₹2,275', trend: '+1.2%', up: true },
                { label: 'Rice (Basmati)', price: '₹4,500', trend: '-0.5%', up: false },
                { label: 'Mustard Seeds', price: '₹5,650', trend: '+2.1%', up: true },
              ].map((m, i) => (
                <div key={i} className="flex items-center justify-between">
                   <div>
                     <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{m.label}</p>
                     <p className="text-base font-bold text-gray-900">{m.price}</p>
                   </div>
                   <span className={`text-[10px] font-bold ${m.up ? 'text-green-600' : 'text-red-500'}`}>
                     {m.up ? '▲' : '▼'} {m.trend}
                   </span>
                </div>
              ))}
            </div>
          </div>

          <div className="app-card p-6 bg-[#1a4d2e] text-white">
             <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
               🏛️ Featured Scheme
             </h3>
             <h4 className="text-lg font-bold mb-2">PM-KISAN Nidhi</h4>
             <p className="text-xs text-white/70 leading-relaxed mb-6">
               Get ₹6,000 yearly directly to your bank account in 3 equal installments.
             </p>
             <Link href="/knowledge" className="text-xs font-bold text-white border-b border-white/30 hover:border-white transition-all pb-1">
               Check Eligibility →
             </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
