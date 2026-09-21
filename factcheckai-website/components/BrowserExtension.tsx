export default function BrowserExtension() {
  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          05 // Browser Integration
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Check claims without leaving your tab</h2>
        <p className="text-lg text-on-surface-variant">
          Select any text on any webpage. Right-click to invoke FactCheckAI. Get instant verdicts with sourced evidence—no tab switching required.
        </p>
      </div>

      {/* Browser Mockup */}
      <div className="bg-surface-container rounded-xl p-6 shadow-2xl">
        <div className="bg-surface-container-low rounded-lg overflow-hidden">
          {/* Browser Chrome */}
          <div className="bg-surface-container-highest p-3 flex items-center gap-3 border-b border-outline-variant/30">
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full bg-error"></div>
              <div className="w-3 h-3 rounded-full bg-tertiary"></div>
              <div className="w-3 h-3 rounded-full bg-secondary"></div>
            </div>
            <div className="flex-1 bg-surface-container px-4 py-1.5 rounded text-xs text-on-surface-variant font-mono">
              https://example-news-site.com/article/breaking-news
            </div>
            <span className="material-symbols-outlined text-surface-tint text-lg">extension</span>
          </div>

          {/* Page Content with Highlighted Claim */}
          <div className="p-6 space-y-4">
            <h3 className="text-xl font-bold text-on-surface">Breaking: New Study Claims...</h3>
            <p className="text-base text-on-surface-variant leading-relaxed">
              According to researchers at the university,{' '}
              <span className="bg-tertiary/20 text-on-surface font-medium px-1 rounded relative">
                "synthetic vitamin supplements are now considered toxic by WHO"
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-error rounded-full animate-pulse"></span>
              </span>
              , sparking controversy in the medical community.
            </p>

            {/* Context Menu Popup */}
            <div className="ml-12 mt-4 bg-surface-container p-4 rounded-lg shadow-2xl border border-outline-variant/30 max-w-md">
              <div className="flex flex-col gap-3">
                <div className="flex items-center gap-2 pb-2 border-b border-outline-variant/30">
                  <span className="material-symbols-outlined text-surface-tint text-lg">fact_check</span>
                  <span className="text-sm font-semibold text-on-surface">FactCheckAI</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="material-symbols-outlined text-error text-base">cancel</span>
                  <span className="font-semibold text-error">VERDICT: FAKE (87% confidence)</span>
                </div>
                <p className="text-xs text-on-surface-variant leading-relaxed">
                  No WHO declaration matches this claim. Cross-referenced with 3 official sources showing no toxicity classification exists.
                </p>
                <button className="bg-primary-container text-on-primary-fixed text-xs font-semibold px-3 py-1.5 rounded hover:bg-surface-tint transition-colors">
                  View Full Analysis
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-surface-tint">bolt</span>
          <h4 className="text-lg font-semibold text-on-surface">Instant Context Menu</h4>
          <p className="text-sm text-on-surface-variant">
            Right-click any selected text to trigger instant fact-checking without opening new tabs.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-secondary">highlight</span>
          <h4 className="text-lg font-semibold text-on-surface">Visual Highlights</h4>
          <p className="text-sm text-on-surface-variant">
            Suspicious claims are automatically highlighted with color-coded severity indicators.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-tertiary">history</span>
          <h4 className="text-lg font-semibold text-on-surface">Session History</h4>
          <p className="text-sm text-on-surface-variant">
            Review all fact-checks from your browsing session with full evidence trails.
          </p>
        </div>
      </div>
    </section>
  );
}
