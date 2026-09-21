export default function HeroSection() {
  return (
    <section className="relative py-8 md:py-12 overflow-hidden" id="product">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Column: Copy & Actions */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Trust Label */}
          <div className="inline-flex items-center gap-2 self-start px-3 py-1 rounded-full bg-surface-container-high">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
            </span>
            <span className="text-xs uppercase tracking-wider text-on-surface-variant font-mono">
              AI-Assisted Fact Verification
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl md:text-5xl font-bold text-on-surface tracking-tight max-w-2xl">
            Verify what you read. <br className="hidden sm:inline" />
            <span className="text-surface-tint">Before you believe it.</span>
          </h1>

          {/* Supporting Copy */}
          <p className="text-lg text-on-surface-variant max-w-xl">
            FactCheckAI uses fine-tuned transformers, hybrid dense-retrieval evidence, and calibrated probabilistic reasoning to help you inspect dubious claims directly within your browsing workflow.
          </p>

          {/* Dual CTA */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <a
              href="#install"
              className="inline-flex items-center gap-2 bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-base font-semibold px-6 py-2.5 rounded shadow-sm transition-colors"
            >
              <span className="material-symbols-outlined text-xl">extension</span>
              <span>Install Extension</span>
              <span className="text-xs bg-on-primary-fixed/15 text-on-primary-fixed px-1.5 py-0.5 rounded tracking-wide font-mono">
                Free OSS
              </span>
            </a>

            <a
              href="https://github.com/BharatChandra-sys/FactCheckAI"
              target="_blank"
              className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-on-surface text-base font-medium px-4 py-2.5 rounded transition-colors shadow-sm"
            >
              <svg className="w-4 h-4 fill-current text-on-surface-variant" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
              <span>View on GitHub</span>
              <span className="inline-flex items-center gap-1 text-xs text-tertiary bg-surface-container-lowest px-1.5 py-0.5 rounded">
                ★ 1.8k
              </span>
            </a>
          </div>

          {/* Metric Badges Row */}
          <div className="flex flex-wrap items-center gap-6 pt-2 text-on-surface-variant text-sm">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-base text-secondary">verified_user</span>
              <span>Zero Data Logging</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-base text-surface-tint">speed</span>
              <span>&lt;240ms Inference</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-base text-tertiary">balance</span>
              <span>Probabilistic Uncertainty</span>
            </div>
          </div>
        </div>

        {/* Right Column: Interactive Browser Extension Card */}
        <div className="lg:col-span-5 flex justify-center">
          <div className="w-full max-w-[430px] rounded-xl bg-surface-container p-4 shadow-2xl flex flex-col gap-4">
            {/* Extension Header */}
            <div className="flex items-center justify-between pb-2">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-lg text-surface-tint">fact_check</span>
                <span className="text-sm font-semibold text-on-surface">FactCheckAI</span>
                <span className="text-xs bg-surface-container-highest text-on-surface-variant px-1.5 py-0.5 rounded">
                  Extension
                </span>
              </div>
              <div className="flex items-center gap-1 bg-surface-container-lowest px-2 py-0.5 rounded text-xs text-on-surface-variant">
                <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                <span>Active DOM</span>
              </div>
            </div>

            {/* Highlight Target Origin */}
            <div className="bg-surface-container-low p-2 rounded flex items-center justify-between text-on-surface-variant text-xs">
              <span className="truncate max-w-[240px]">en.wikipedia.org / social_thread#8402</span>
              <span className="text-outline uppercase">Selected span</span>
            </div>

            {/* The Evaluated Claim */}
            <div className="bg-surface-container-lowest p-3 rounded flex flex-col gap-1">
              <span className="text-xs text-outline uppercase tracking-wider">Claim detected:</span>
              <p className="text-sm text-on-surface font-medium italic">
                "5G towers spread coronavirus through high-frequency radio waves."
              </p>
            </div>

            {/* Verdict Block: FAKE */}
            <div className="p-3 rounded bg-error-container/20 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-lg text-error">cancel</span>
                  <span className="text-sm font-semibold text-error uppercase tracking-wider">VERDICT: FAKE</span>
                </div>
                <span className="text-sm text-error font-mono">87.4% CONFIDENCE</span>
              </div>
              {/* Horizontal Segmented Confidence Meter */}
              <div className="w-full bg-surface-container-highest h-1.5 rounded-full overflow-hidden flex">
                <div className="bg-error h-full rounded-full" style={{ width: '87.4%' }}></div>
              </div>
            </div>

            {/* Short Scientific Explanation */}
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Multiple international public health authorities and telecommunications engineering bodies confirm non-ionizing electromagnetic radiation cannot synthesize or transmit biological viral matter.
            </p>

            {/* Evidence List */}
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center justify-between text-on-surface-variant text-xs pb-1">
                <span className="uppercase tracking-wider">Top Validated Sources</span>
                <span>Vector Sim: 0.94</span>
              </div>

              {/* Source 1 */}
              <div className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs">
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-on-surface truncate font-medium">WHO Global Health Brief (2020)</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">98% STRENGTH</span>
              </div>

              {/* Source 2 */}
              <div className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs">
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-on-surface truncate font-medium">IEEE Microwave Theory Report</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">94% STRENGTH</span>
              </div>

              {/* Source 3 */}
              <div className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs">
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-on-surface truncate font-medium">Reuters Fact Verification Archive</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">91% STRENGTH</span>
              </div>
            </div>

            {/* Popup Action Footer */}
            <div className="flex items-center justify-between pt-2 text-xs text-outline">
              <span className="font-mono">RoBERTa-v2 + Hybrid RAG</span>
              <div className="flex items-center gap-2">
                <button className="px-2 py-1 bg-surface-container-high hover:bg-surface-container-highest text-on-surface rounded transition-colors">
                  Reasoning Chain
                </button>
                <button className="px-2 py-1 bg-primary-container text-on-primary-fixed font-semibold rounded hover:bg-surface-tint transition-colors">
                  View All (3)
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
