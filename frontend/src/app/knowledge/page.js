'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/context/LanguageContext';

const catColors = {
  Fertilizer: 'bg-green-100 text-green-700',
  'Soil Health': 'bg-amber-100 text-amber-700',
  'Water Management': 'bg-blue-100 text-blue-700',
  Technique: 'bg-purple-100 text-purple-700',
  Season: 'bg-emerald-100 text-emerald-700',
};

/**
 * Knowledge Garden - Agricultural Dictionary & Resource Center
 * Provides multilingual definitions of core farming terms.
 */
export default function KnowledgePage() {
  const [tab, setTab] = useState('dictionary');
  const [terms, setTerms] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [selectedTerm, setSelectedTerm] = useState(null);
  const { language: lang, t } = useLanguage();
  
  const categoryMap = {
    'All': t('all_categories'),
    'Fertilizer': t('category_fertilizer'),
    'Soil Health': t('category_soil'),
    'Water Management': t('category_water'),
    'Technique': t('category_technique'),
    'Season': t('category_season'),
  };
  useEffect(() => {
    // Fetch Multilingual Knowledge Garden
      const fetchKnowledge = async () => {
      const apiHost = window.location.hostname;
      try {
        setLoading(true);
        const res = await fetch(`http://${apiHost}:8000/api/knowledge-garden?t=${new Date().getTime()}`, { cache: 'no-store' });
        const data = await res.json();
        setTerms(data.terms || []);
      } catch (err) {
        console.error("Failed to fetch knowledge garden:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchKnowledge();
  }, []);

  // Filter logic
  const filteredTerms = terms.filter(t => {
    const searchLower = search.toLowerCase();
    
    // If there is no search query, just filter by category
    if (!searchLower) {
      return category === 'All' || t.category === category;
    }

    // Check names in all languages
    const nameMatch = 
      (t.name['en'] && t.name['en'].toLowerCase().includes(searchLower)) ||
      (t.name['hi'] && t.name['hi'].toLowerCase().includes(searchLower)) ||
      (t.name['kn'] && t.name['kn'].toLowerCase().includes(searchLower)) ||
      (t.id && t.id.toLowerCase().includes(searchLower));

    // Check definitions in the current language
    const defMatch = t.definition[lang] && t.definition[lang].toLowerCase().includes(searchLower);

    const matchesSearch = nameMatch || defMatch;
    const matchesCategory = category === 'All' || t.category === category;
    
    return matchesSearch && matchesCategory;
  });

  // Only show categories of core terms in the dropdown to keep it clean
  const categories = ['All', ...new Set(terms.filter(t => ['npk', 'soil_ph', 'irrigation', 'crop_rotation', 'vermicompost', 'mulching', 'kharif', 'rabi', 'pesticide'].includes(t.id)).map(t => t.category))];

  return (
    <div className="max-w-6xl mx-auto space-y-10 animate-fade-in pb-20">
      
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-100 pb-8">
        <div>
          <h1 className="text-4xl font-black text-gray-900 tracking-tight">{t('knowledge_garden')}</h1>
          <p className="text-gray-500 mt-2 font-medium">{t('knowledge_desc')}</p>
        </div>
        <div className="flex bg-gray-50 p-1.5 rounded-2xl border border-gray-100">
          <button 
            className={`px-6 py-2.5 rounded-xl font-bold text-sm transition-all flex items-center gap-2 ${tab === 'dictionary' ? 'bg-[#1a4d2e] text-white shadow-lg' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <span>📖</span> {t('dictionary')}
          </button>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="grid md:grid-cols-4 gap-4">
        <div className="md:col-span-3 relative group">
          <span className="absolute left-5 top-1/2 -translate-y-1/2 text-xl transition-transform group-focus-within:scale-110">🔍</span>
          <input
            type="text" value={search} onChange={e => setSearch(e.target.value)}
            placeholder={t('search_terms')}
            className="w-full bg-white border border-gray-100 rounded-[1.5rem] pl-14 pr-6 py-4 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-[#1a4d2e]/5 transition-all shadow-sm"
          />
        </div>
        <select 
          value={category} onChange={e => setCategory(e.target.value)}
          className="bg-white border border-gray-100 rounded-[1.5rem] px-6 py-4 text-gray-600 font-bold text-sm focus:outline-none focus:ring-4 focus:ring-[#1a4d2e]/5 shadow-sm appearance-none cursor-pointer"
        >
          {categories.map(c => <option key={c} value={c}>{categoryMap[c] || c}</option>)}
        </select>
      </div>

      {/* Grid Content */}
      {loading ? (
        <div className="flex justify-center py-20">
           <div className="w-10 h-10 border-4 border-[#1a4d2e]/10 border-t-[#1a4d2e] rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTerms.length === 0 ? (
            <div className="col-span-full py-20 text-center text-gray-400 italic">
               {t('no_terms')}
            </div>
          ) : (
            filteredTerms.map(term => (
              <div 
                key={term.id} 
                onClick={() => setSelectedTerm(term)}
                className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-50 flex flex-col hover:shadow-xl hover:translate-y-[-4px] transition-all group cursor-pointer"
              >
                <div className="mb-6 flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${catColors[term.category] || 'bg-gray-100 text-gray-600'}`}>
                    {categoryMap[term.category] || term.category}
                  </span>
                  <span className="text-lg opacity-0 group-hover:opacity-100 transition-opacity">✨</span>
                </div>
                
                <h3 className="text-2xl font-black text-gray-900 mb-3 tracking-tight">
                  {term.name[lang] || term.name['en']}
                </h3>
                
                <p className="text-sm text-gray-500 leading-relaxed font-medium mb-6 flex-1">
                  {term.definition[lang] || term.definition['en']}
                </p>

                <div className="pt-6 border-t border-gray-50 flex items-center justify-between">
                   <div className="flex gap-1.5">
                      <span className="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center text-[10px] font-bold text-blue-400" title="English Ready">EN</span>
                      <span className="w-6 h-6 rounded-full bg-green-50 flex items-center justify-center text-[10px] font-bold text-green-400" title="Kannada Ready">KN</span>
                      <span className="w-6 h-6 rounded-full bg-orange-50 flex items-center justify-center text-[10px] font-bold text-orange-400" title="Hindi Ready">HI</span>
                   </div>
                   <span className="text-[10px] font-black text-gray-300 uppercase tracking-widest">{t('verified_info')}</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Info Card */}
      <div className="bg-[#1a4d2e] p-10 rounded-[3rem] text-white shadow-2xl relative overflow-hidden flex flex-col md:flex-row items-center gap-10">
         <div className="absolute -top-10 -left-10 w-40 h-40 bg-white/5 rounded-full blur-3xl" />
         <div className="text-5xl">💡</div>
         <div className="flex-1 text-center md:text-left">
            <h3 className="text-2xl font-black mb-2 tracking-tight">{t('did_you_know')}</h3>
            <p className="text-white/70 font-medium leading-relaxed max-w-2xl text-sm">
               {t('soil_ph_fact')}
            </p>
         </div>
      </div>

      {/* Detail Modal */}
      {selectedTerm && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white max-w-2xl w-full rounded-[2.5rem] p-8 relative shadow-2xl animate-fade-in">
            <button 
              onClick={() => setSelectedTerm(null)}
              className="absolute top-6 right-6 w-10 h-10 bg-gray-50 text-gray-500 rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors"
            >
              ✖
            </button>
            <div className="mb-6 flex items-center gap-4">
               <span className={`px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest ${catColors[selectedTerm.category] || 'bg-gray-100 text-gray-600'}`}>
                 {categoryMap[selectedTerm.category] || selectedTerm.category}
               </span>
            </div>
            <h2 className="text-3xl font-black text-gray-900 mb-6">
               {selectedTerm.name[lang] || selectedTerm.name['en']}
            </h2>
            
            <div className="space-y-6">
               <div>
                  <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-2">{t('definition_label')}</h4>
                  <p className="text-gray-700 text-lg leading-relaxed font-medium">
                     {selectedTerm.definition[lang] || selectedTerm.definition['en']}
                  </p>
               </div>
               
               {selectedTerm.simple && (
                 <div className="bg-[#1a4d2e]/5 p-5 rounded-2xl border border-[#1a4d2e]/10">
                    <h4 className="text-xs font-bold text-[#1a4d2e] uppercase tracking-widest mb-2 flex items-center gap-2"><span>💡</span> {t('simple_explanation')}</h4>
                    <p className="text-gray-800 font-medium">
                       {selectedTerm.simple[lang] || selectedTerm.simple['en']}
                    </p>
                 </div>
               )}

               {selectedTerm.usage && (
                 <div>
                    <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-2">{t('how_to_use')}</h4>
                    <p className="text-gray-600 font-medium bg-gray-50 p-5 rounded-2xl border border-gray-100">
                       {selectedTerm.usage[lang] || selectedTerm.usage['en']}
                    </p>
                 </div>
               )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
