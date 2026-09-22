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
          <Link href="/#product" className="text-sm text-on-surface font-semibold bg-surface-container-high rounded px-3 py-1.5 transition-colors">
            Product
          </Link>
          <Link href="/#how-it-works" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 px-2">
            How It Works
          </Link>
          <Link href="/#technology" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 px-2">
            Technology
          </Link>
          <Link href="https://github.com/BharatChandra-sys/FactCheckAI" target="_blank" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 px-2">
            GitHub
          </Link>
          <Link href="/privacy" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 px-2">
            Privacy
          </Link>
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-2 sm:gap-4 shrink-0">
          <a
            href="https://chrome.google.com/webstore/category/extensions"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-sm font-semibold px-4 py-1.5 rounded transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-container"
          >
            <span className="material-symbols-outlined text-lg">extension</span>
            <span>Get Extension</span>
          </a>
        </div>
      </div>
    </header>
  );
}
