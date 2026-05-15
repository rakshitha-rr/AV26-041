'use client';

import './globals.css';
import Sidebar from '@/components/Sidebar';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { LanguageProvider } from '@/context/LanguageContext';
import LanguageSwitcher from '@/components/LanguageSwitcher';

export default function RootLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();
  const isLoginPage = pathname === '/login';

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <title>AgriIntel — Modern Farm Management</title>
        <meta name="description" content="Clean, professional farming assistant for modern agriculture." />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌾</text></svg>" />
      </head>
      <body suppressHydrationWarning className={`flex h-screen overflow-hidden ${isLoginPage ? 'bg-black' : 'bg-[#f8faf8]'}`}>
        <LanguageProvider>
          {!isLoginPage && (
            <>
              {/* Mobile overlay */}
              {sidebarOpen && (
                <div className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 lg:hidden" onClick={() => setSidebarOpen(false)} />
              )}

              {/* Sidebar */}
              <div className={`fixed lg:static inset-y-0 left-0 z-40 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 transition-transform duration-300 ease-in-out`}>
                <Sidebar onClose={() => setSidebarOpen(false)} />
              </div>
            </>
          )}

          {/* Main content */}
          <main className="flex-1 overflow-y-auto flex flex-col">
            {/* Header / Top Bar */}
            {!isLoginPage && (
              <div className="sticky top-0 z-20 bg-white/80 backdrop-blur-xl border-b border-gray-100 px-6 lg:px-10 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 hover:bg-gray-100 rounded-lg">
                    <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                  <span className="hidden lg:inline text-xs font-bold text-gray-400 uppercase tracking-[0.3em]">AgriIntel Smart System</span>
                </div>
                
                {/* Global Language Switcher */}
                <LanguageSwitcher />
              </div>
            )}
            
            <div className={`${isLoginPage ? 'p-0 h-full' : 'p-6 lg:p-10'} flex-1 max-w-7xl mx-auto w-full`}>
              {children}
            </div>
          </main>
        </LanguageProvider>
      </body>
    </html>
  );
}
