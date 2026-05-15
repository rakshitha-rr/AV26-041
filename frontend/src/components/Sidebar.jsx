'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useLanguage } from '@/context/LanguageContext';

export default function Sidebar({ onClose }) {
  const pathname = usePathname();
  const { language, t } = useLanguage();

  const navItems = [
    { href: '/', label: t('dashboard'), icon: '🏠' },
    { href: '/chatbot', label: t('advisor'), icon: '🤖' },
    { href: '/knowledge', label: t('knowledge'), icon: '📚' },
    { href: '/heatmap', label: t('heatmap'), icon: '🗺️' },
    { href: '/sms', label: t('offline'), icon: '📡' },
  ];

  return (
    <aside className="w-64 h-screen bg-white border-r border-gray-200 flex flex-col">
      <div className="p-8">
        <h1 className="text-xl font-extrabold text-[#1a4d2e] tracking-tight">
          AgriIntel
        </h1>
        <p className="text-[11px] text-gray-400 font-bold uppercase tracking-widest mt-1">{t('version_text')}</p>
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            onClick={onClose}
            className={`flex items-center gap-4 px-5 py-4 rounded-2xl transition-all font-bold text-sm ${
              pathname === item.href 
                ? 'bg-[#1a4d2e] text-white shadow-lg shadow-green-900/20' 
                : 'text-gray-400 hover:bg-gray-50 hover:text-gray-900'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="p-6 space-y-6">
        <div className="p-4 bg-gray-50 rounded-2xl border border-gray-100">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
            <span className="text-[10px] font-bold text-gray-500 uppercase">{t('system_ready')}</span>
          </div>
          <p className="text-[10px] text-gray-400">{t('stable_connection')}</p>
        </div>

        <button 
          suppressHydrationWarning
          onClick={() => {
            localStorage.removeItem('agri_token');
            localStorage.removeItem('farmer_aadhaar');
            window.location.reload();
          }}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-red-500 hover:bg-red-50 font-bold text-sm transition-all"
        >
          <span>🚪</span>
          <span>{t('logout')}</span>
        </button>
      </div>
    </aside>
  );
}
