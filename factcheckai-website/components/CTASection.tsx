export default function CTASection() {
  return (
    <section className="py-12 md:py-16">
      <div className="bg-linear-to-br from-surface-container to-surface-container-high rounded-2xl p-8 md:p-12 text-center flex flex-col items-center gap-6 shadow-2xl">
        {/* Icon Badge */}
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-container">
          <span className="material-symbols-outlined text-3xl text-on-primary-fixed">verified</span>
        </div>

        {/* Headline */}
        <h2 className="text-3xl md:text-5xl font-bold text-on-surface max-w-3xl">
          Ready to verify the web?
        </h2>

        {/* Supporting Text */}
        <p className="text-lg text-on-surface-variant max-w-2xl">
          Install FactCheckAI in seconds. Free, open-source, and privacy-respecting. Start fact-checking claims directly in your browser today.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <a
            href="#install"
            className="inline-flex items-center gap-2 bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-lg font-semibold px-8 py-3 rounded-lg shadow-lg transition-colors"
          >
            <span className="material-symbols-outlined text-2xl">extension</span>
            <span>Install Extension</span>
          </a>
          <a
            href="https://github.com/yourusername/factcheckai"
            target="_blank"
            className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-on-surface text-lg font-medium px-8 py-3 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            <span>View on GitHub</span>
          </a>
        </div>

        {/* Trust Badges */}
        <div className="flex flex-wrap items-center justify-center gap-6 pt-4 text-on-surface-variant text-sm">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-base text-secondary">verified_user</span>
            <span>MIT License</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-base text-surface-tint">shield</span>
            <span>Zero Data Collection</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-base text-tertiary">groups</span>
            <span>342+ Contributors</span>
          </div>
        </div>
      </div>
    </section>
  );
}
