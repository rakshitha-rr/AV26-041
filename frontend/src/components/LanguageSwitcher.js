'use client';

import { useLanguage } from '@/context/LanguageContext';

export default function LanguageSwitcher() {
  const { language, switchLanguage } = useLanguage();

  const langs = [
    { code: 'en', label: 'English' },
    { code: 'kn', label: 'ಕನ್ನಡ' },
    { code: 'hi', label: 'हिंदी' },
  ];

  return (
    <div className="flex bg-gray-100 p-1 rounded-2xl border border-gray-200">
      {langs.map((l) => (
        <button
          key={l.code}
          suppressHydrationWarning
          onClick={() => switchLanguage(l.code)}
          className={`px-5 py-2 rounded-xl text-xs font-black transition-all ${
            language === l.code
              ? 'bg-[#1a4d2e] text-white shadow-lg'
              : 'text-gray-400 hover:text-gray-600'
          }`}
        >
          {l.label}
        </button>
      ))}
    </div>
  );
}
