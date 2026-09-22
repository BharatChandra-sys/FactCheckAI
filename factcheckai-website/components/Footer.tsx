import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="w-full bg-surface-container-low border-t border-outline-variant/30 mt-12">
      <div className="max-w-7xl mx-auto px-4 md:px-8 lg:px-12 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Column */}
          <div className="flex flex-col gap-4">
            <span className="text-xl font-bold text-white">
              FactCheck<span className="text-brand-yellow">AI</span>
            </span>
            <p className="text-sm text-on-surface-variant max-w-xs">
              AI-powered fact verification for everyone. We help you separate truth from fiction while you browse the web.
            </p>
            <div className="flex items-center gap-3">
              <a href="mailto:contact@gari.live" className="text-on-surface-variant hover:text-on-surface transition-colors" title="Email us">
                <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
              </a>
              <a href="https://gari.live" target="_blank" className="text-on-surface-variant hover:text-on-surface transition-colors" title="Visit website">
                <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Product Column */}
          <div className="flex flex-col gap-3">
            <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider">Features</h3>
            <Link href="/#product" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Real-time Checking
            </Link>
            <Link href="/#how-it-works" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              How It Works
            </Link>
            <Link href="/#technology" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Our Technology
            </Link>
            <a href="https://chrome.google.com/webstore/category/extensions" target="_blank" rel="noopener noreferrer" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Download
            </a>
          </div>

          {/* Resources Column */}
          <div className="flex flex-col gap-3">
            <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider">Contact</h3>
            <a href="mailto:contact@gari.live" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Email Support
            </a>
            <a href="https://gari.live" target="_blank" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Official Website
            </a>
            <Link href="/support" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Help Center
            </Link>
          </div>

          {/* Legal Column */}
          <div className="flex flex-col gap-3">
            <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider">Legal</h3>
            <Link href="/privacy" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Terms of Service
            </Link>
            <Link href="/support" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors">
              Support
            </Link>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-outline-variant/30 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-on-surface-variant">
            © {new Date().getFullYear()} FactCheckAI. All rights reserved.
          </p>
          <div className="flex items-center gap-6 text-sm text-on-surface-variant">
            <span className="flex items-center gap-2">
              <span className="material-symbols-outlined text-base text-secondary">verified_user</span>
              Zero Data Collection
            </span>
            <span className="flex items-center gap-2">
              <span className="material-symbols-outlined text-base text-surface-tint">speed</span>
              AI-Powered Verification
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
