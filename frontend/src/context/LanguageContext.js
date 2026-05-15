'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from '@/utils/translations';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    const saved = localStorage.getItem('agri_lang');
    if (saved) setLanguage(saved);
  }, []);

  const switchLanguage = (lang) => {
    setLanguage(lang);
    localStorage.setItem('agri_lang', lang);
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined) return '';
    const str = num.toString();
    
    const digitMaps = {
      kn: ['೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'],
      hi: ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
      en: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    };

    const map = digitMaps[language] || digitMaps['en'];
    return str.split('').map(char => {
      const digit = parseInt(char);
      return isNaN(digit) ? char : map[digit];
    }).join('');
  };

  const t = (key) => {
    return translations[language][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, switchLanguage, t, formatNumber }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
