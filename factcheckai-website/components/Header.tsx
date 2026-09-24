'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-surface/85 glass-morphism border-b border-outline-variant/30">
      <div className="h-16 max-w-7xl mx-auto px-4 md:px-8 lg:px-12 flex items-center justify-between gap-4">
        {/* Logo */}
        <div className="flex items-center gap-4 shrink-0">
          <Link href="/" className="flex items-center gap-3 group focus:outline-none">
            <span className="text-xl font-bold tracking-tight text-white">
              FactCheck<span className="text-brand-yellow">AI</span>
            </span>
          </Link>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-6">
          <a 
            href="#product" 
            onClick={(e) => {
              e.preventDefault();
              document.getElementById('product')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
            className="text-sm text-white font-semibold bg-surface-container-high rounded px-3 py-1.5 transition-colors cursor-pointer"
          >
            Product
          </a>
          <a 
            href="#how-it-works" 
            onClick={(e) => {
              e.preventDefault();
              document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
            className="text-sm text-on-surface-variant hover:text-white transition-colors py-1.5 px-2 cursor-pointer"
          >
            How It Works
          </a>
          <a 
            href="#technology" 
            onClick={(e) => {
              e.preventDefault();
              document.getElementById('technology')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
            className="text-sm text-on-surface-variant hover:text-white transition-colors py-1.5 px-2 cursor-pointer"
          >
            Technology
          </a>
          <Link href="https://github.com/BharatChandra-sys/FactCheckAI" target="_blank" className="text-sm text-on-surface-variant hover:text-white transition-colors py-1.5 px-2">
            GitHub
          </Link>
          <Link href="/privacy" className="text-sm text-on-surface-variant hover:text-white transition-colors py-1.5 px-2">
            Privacy
          </Link>
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-2 sm:gap-4 shrink-0">
          <a
            href="/install"
            className="flex items-center gap-2 bg-brand-yellow hover:bg-brand-orange text-black text-sm font-semibold px-4 py-1.5 rounded transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-yellow"
          >
            <span className="material-symbols-outlined text-lg">extension</span>
            <span>Get Extension</span>
          </a>
        </div>
      </div>
    </header>
  );
}
