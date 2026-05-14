'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';

const navItems = [
  { href: '/', label: 'Dashboard', icon: '🏠' },
  { href: '/chatbot', label: 'Farming Advisor', icon: '🤖' },
  { href: '/knowledge', label: 'Resources', icon: '📚' },
  { href: '/sms', label: 'Offline Bridge', icon: '📡' },
];

const languages = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिन्दी' },
  { code: 'kn', label: 'ಕನ್ನಡ' },
];

export default function Sidebar({ onClose }) {
  const pathname = usePathname();
  const [lang, setLang] = useState('en');

  useEffect(() => {
    const savedLang = localStorage.getItem('agri_lang') || 'en';
    setLang(savedLang);
  }, []);

  const handleLangChange = (newLang) => {
    setLang(newLang);
    localStorage.setItem('agri_lang', newLang);
  };

  return (
    <aside className="w-64 h-screen bg-white border-r border-gray-200 flex flex-col">
      <div className="p-8">
        <h1 className="text-xl font-extrabold text-[#1a4d2e] tracking-tight">
          AgriAssist
        </h1>
        <p className="text-[11px] text-gray-400 font-bold uppercase tracking-widest mt-1">v1.0.4 Release</p>
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            onClick={onClose}
            className={`nav-link ${pathname === item.href ? 'active' : ''}`}
          >
            <span className="text-lg opacity-80">{item.icon}</span>
            <span className="text-sm font-semibold">{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="p-6 space-y-6">
        <div>
          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3 ml-1">Interface Language</p>
          <select
            value={lang}
            onChange={(e) => handleLangChange(e.target.value)}
            className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 text-xs font-bold text-gray-600 focus:outline-none focus:border-[#1a4d2e]"
          >
            {languages.map((l) => (
              <option key={l.code} value={l.code}>{l.label}</option>
            ))}
          </select>
        </div>

        <div className="p-4 bg-gray-50 rounded-2xl border border-gray-100">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
            <span className="text-[10px] font-bold text-gray-500 uppercase">System Ready</span>
          </div>
          <p className="text-[10px] text-gray-400">Stable connection established with server.</p>
        </div>
      </div>
    </aside>
  );
}
