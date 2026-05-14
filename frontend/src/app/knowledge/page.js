'use client';
import { useState, useEffect } from 'react';

const catColors = {
  Soil: 'badge-success', Crops: 'badge-warning', Irrigation: 'badge-info',
  'Pest Management': 'badge-danger', Seasons: 'badge-warning', Economics: 'badge-success',
  Technology: 'badge-info', 'Post-Harvest': 'badge-warning',
  'Financial Support': 'badge-success', Insurance: 'badge-info', Infrastructure: 'badge-warning',
  'Organic Farming': 'badge-success', Marketing: 'badge-info',
};

export default function KnowledgePage() {
  const [tab, setTab] = useState('dictionary');
  const [terms, setTerms] = useState([]);
  const [schemes, setSchemes] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [categories, setCategories] = useState([]);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const url = tab === 'dictionary' 
      ? `/api/terms?search=${search}&category=${category}` 
      : `/api/schemes?category=${category}`;
    
    fetch(url).then(r => r.json()).then(d => {
      if (tab === 'dictionary') { setTerms(d.terms || []); setCategories(d.categories || []); }
      else { setSchemes(d.schemes || []); setCategories(d.categories || []); }
    }).catch(() => {});
  }, [tab, search, category]);

  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-fade-in">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-gray-200 pb-8">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Agricultural Resources</h1>
          <p className="text-gray-500 mt-2 font-medium">Explore modern farming techniques and government initiatives.</p>
        </div>
        <div className="flex bg-gray-100 p-1 rounded-xl">
          {[
            { id: 'dictionary', label: 'Dictionary', icon: '📖' },
            { id: 'schemes', label: 'Gov Schemes', icon: '🏛️' }
          ].map(t => (
            <button 
              key={t.id} 
              onClick={() => { setTab(t.id); setCategory('All'); setSearch(''); setExpandedId(null); }}
              className={`px-6 py-2 rounded-lg font-bold text-sm transition-all flex items-center gap-2 ${tab === t.id ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <span className="text-base">{t.icon}</span>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="grid md:grid-cols-4 gap-4">
        <div className="md:col-span-3 relative">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            type="text" value={search} onChange={e => setSearch(e.target.value)}
            placeholder={`Search ${tab === 'dictionary' ? 'technical terms...' : 'schemes...'}`}
            className="w-full bg-white border border-gray-200 rounded-xl pl-12 pr-4 py-3.5 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#1a4d2e] transition-all shadow-sm"
          />
        </div>
        <select 
          value={category} onChange={e => setCategory(e.target.value)}
          className="bg-white border border-gray-200 rounded-xl px-4 py-3.5 text-gray-600 font-bold text-sm focus:outline-none focus:border-[#1a4d2e] shadow-sm"
        >
          <option value="All">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      {/* Content Area */}
      {tab === 'dictionary' && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {terms.map(term => (
            <div 
              key={term.id} 
              className={`app-card p-6 flex flex-col cursor-pointer transition-all ${expandedId === term.id ? 'ring-2 ring-[#1a4d2e] ring-offset-2' : ''}`}
              onClick={() => setExpandedId(expandedId === term.id ? null : term.id)}
            >
              <div className="mb-4">
                <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest ${catColors[term.category] || 'bg-gray-100 text-gray-600'}`}>
                  {term.category}
                </span>
              </div>
              <h3 className="text-lg font-extrabold text-gray-900 mb-2">{term.term}</h3>
              <p className={`text-sm text-gray-500 leading-relaxed ${expandedId === term.id ? '' : 'line-clamp-3'}`}>
                {term.definition}
              </p>
              {expandedId === term.id && (
                <div className="mt-6 pt-6 border-t border-gray-100 animate-fade-in space-y-4">
                  <div>
                    <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Related</p>
                    <div className="flex flex-wrap gap-1.5">
                      {term.relatedTerms?.map((rt, i) => (
                        <span key={i} className="px-2 py-1 bg-gray-50 border border-gray-100 text-gray-500 text-[10px] font-bold rounded-lg uppercase tracking-tighter">
                          {rt}
                        </span>
                      ))}
                    </div>
                  </div>
                  <button className="w-full py-2.5 bg-[#1a4d2e] text-white text-xs font-bold rounded-xl shadow-md shadow-green-900/10">
                    Bookmark Item
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {tab === 'schemes' && (
        <div className="space-y-6">
          {schemes.filter(s => !search || s.name.toLowerCase().includes(search.toLowerCase()) || s.fullName.toLowerCase().includes(search.toLowerCase()))
            .map(scheme => (
            <div 
              key={scheme.id} 
              className={`app-card overflow-hidden transition-all cursor-pointer ${expandedId === `s${scheme.id}` ? 'ring-2 ring-blue-600 ring-offset-2' : ''}`}
              onClick={() => setExpandedId(expandedId === `s${scheme.id}` ? null : `s${scheme.id}`)}
            >
              <div className="p-8">
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
                  <div className="flex-1">
                    <div className="flex items-center gap-4 mb-4">
                      <span className="px-2.5 py-1 bg-blue-50 text-blue-700 text-[10px] font-bold uppercase tracking-widest rounded">
                        {scheme.category}
                      </span>
                      <span className="text-sm font-bold text-emerald-600">
                        {scheme.amount}
                      </span>
                    </div>
                    <h3 className="text-2xl font-black text-gray-900 mb-1">{scheme.name}</h3>
                    <p className="text-sm text-gray-400 font-bold uppercase tracking-tighter mb-4 opacity-75">{scheme.fullName}</p>
                    <p className="text-gray-500 leading-relaxed max-w-3xl font-medium">
                      {scheme.description}
                    </p>
                  </div>
                  <div className={`w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center transition-transform duration-300 ${expandedId === `s${scheme.id}` ? 'rotate-180 bg-blue-50 text-blue-600' : 'text-gray-400'}`}>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" /></svg>
                  </div>
                </div>

                {expandedId === `s${scheme.id}` && (
                  <div className="mt-10 pt-10 border-t border-gray-100 grid md:grid-cols-2 gap-12 animate-fade-in">
                    <div className="space-y-6">
                      <h4 className="text-sm font-bold text-gray-900 uppercase tracking-widest flex items-center gap-2">
                        <span className="w-1.5 h-1.5 bg-green-600 rounded-full" />
                        Program Benefits
                      </h4>
                      <div className="grid gap-3">
                        {scheme.benefits.map((b, i) => (
                          <div key={i} className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl border border-gray-100">
                            <span className="text-green-600 text-lg mt-0.5">✓</span>
                            <p className="text-sm text-gray-700 font-medium">{b}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="space-y-8">
                      <div>
                        <h4 className="text-sm font-bold text-gray-900 uppercase tracking-widest flex items-center gap-2 mb-4">
                          <span className="w-1.5 h-1.5 bg-blue-600 rounded-full" />
                          Requirements
                        </h4>
                        <div className="p-5 bg-blue-50/30 border border-blue-100 rounded-xl">
                          <p className="text-sm text-gray-600 leading-relaxed font-medium">{scheme.eligibility}</p>
                        </div>
                      </div>
                      <div className="flex gap-4">
                        <a href={scheme.link} target="_blank" rel="noopener" className="flex-1 btn-primary text-center flex items-center justify-center gap-2 shadow-lg shadow-green-900/20" onClick={(e) => e.stopPropagation()}>
                          Official Portal 🔗
                        </a>
                        <button className="btn-secondary px-8" onClick={(e) => { e.stopPropagation(); alert('Guide saved!'); }}>
                          PDF
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
