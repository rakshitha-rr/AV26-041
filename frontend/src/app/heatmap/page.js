'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLanguage } from '@/context/LanguageContext';

export default function HeatmapPage() {
  const { language, t, formatNumber } = useLanguage();
  const lang = language || 'en';
  
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Time simulation states
  const [hourIndex, setHourIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const todayDate = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  
  // Create 24 hour labels (e.g., "00:00", "01:00", ... "23:00")
  const hours = Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2, '0')}:00`);
  
  // Hourly multipliers to simulate changing conditions over the day
  // e.g. Midday heat lowers moisture/stress levels, night is optimal
  const hourlyModifiers = [
    1.10, 1.10, 1.05, 1.05, 1.00, 1.00, // 00:00 - 05:00 (Cool night)
    1.00, 1.00, 0.95, 0.95, 0.90, 0.85, // 06:00 - 11:00 (Morning warming up)
    0.75, 0.65, 0.60, 0.65, 0.70, 0.80, // 12:00 - 17:00 (Peak heat / Stress)
    0.85, 0.90, 0.95, 1.00, 1.05, 1.10  // 18:00 - 23:00 (Cooling down)
  ];

  // Real-time clock state
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const fetchHeatmap = async () => {
      const apiHost = window.location.hostname;
      try {
        const res = await fetch(`http://${apiHost}:8000/api/yield-heatmap`);
        const data = await res.json();
        setZones(data.zones || []);
      } catch (err) {
        console.error('Failed to fetch heatmap', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHeatmap();
  }, []);

  // Real-time ticker
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000); // Update every second to show a live clock
    return () => clearInterval(interval);
  }, []);

  // Derived state: calculate dynamic yields based on current actual hour
  const currentHour = currentTime.getHours();
  
  const dynamicZones = zones.map(zone => {
    const baseYield = zone.predicted_yield;
    const modifier = hourlyModifiers[currentHour];
    // Add a tiny bit of random variation so it feels alive
    const randomVariation = 1 + (Math.random() * 0.04 - 0.02); 
    
    const currentYield = baseYield * modifier * randomVariation;
    
    let colorClass, label;
    if (currentYield >= 4.0) {
      colorClass = 'from-emerald-400 to-green-600 shadow-green-500/50';
      label = t('high_yield');
    } else if (currentYield >= 2.5) {
      colorClass = 'from-amber-300 to-yellow-500 shadow-yellow-500/50';
      label = t('medium_yield');
    } else {
      colorClass = 'from-red-400 to-rose-600 shadow-red-500/50';
      label = t('low_yield');
    }

    return {
      ...zone,
      currentYield: currentYield.toFixed(2),
      colorClass,
      label
    };
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[80vh]">
        <div className="w-12 h-12 border-4 border-[#1a4d2e]/20 border-t-[#1a4d2e] rounded-full animate-spin"></div>
      </div>
    );
  }

  // Format time nicely (e.g., 08:15:30 AM)
  const timeString = currentTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const dateString = currentTime.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in pb-20">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-8 rounded-[2rem] shadow-sm border border-gray-100">
        <div>
          <h1 className="text-3xl font-bold text-[#1a4d2e] tracking-tight mb-2">{t('heatmap_title')}</h1>
          <p className="text-gray-500 text-lg">{t('heatmap_desc')}</p>
        </div>
        
        <div className="flex items-center gap-6 bg-gray-50 px-8 py-5 rounded-2xl border border-gray-100 shadow-inner">
          <div className="flex items-center gap-4">
            <div className="relative flex h-4 w-4">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4 w-4 bg-green-500"></span>
            </div>
            
            <div className="w-48 text-right">
              <p className="text-xs text-gray-400 font-bold uppercase tracking-widest mb-1">{formatNumber(dateString)}</p>
              <div className="text-3xl font-black text-[#1a4d2e] tabular-nums tracking-tight">
                {formatNumber(timeString)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {dynamicZones.map((zone) => (
          <motion.div 
            key={zone.zone_id}
            layout
            transition={{ duration: 0.5 }}
            className={`relative overflow-hidden rounded-2xl p-5 bg-gradient-to-br ${zone.colorClass} text-white shadow-lg transition-all duration-700`}
          >
            <div className="relative z-10">
              <p className="text-white/80 text-xs font-bold tracking-wider uppercase mb-1">{zone.zone_id}</p>
              <h3 className="text-xl font-bold mb-4 line-clamp-1">{zone.zone_name}</h3>
              
              <div className="flex items-end justify-between mt-8">
                <div>
                  <p className="text-white/90 text-xs font-medium mb-1">{t('predicted')}</p>
                  <p className="text-3xl font-black">{formatNumber(zone.currentYield)}</p>
                </div>
                <div className="text-right">
                  <span className="inline-block px-2 py-1 bg-black/20 rounded-lg text-[10px] font-bold uppercase tracking-wider backdrop-blur-sm">
                    {zone.label}
                  </span>
                </div>
              </div>
            </div>
            
            {/* Decorative background circle */}
            <div className="absolute -bottom-6 -right-6 w-24 h-24 bg-white/10 rounded-full blur-xl"></div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
