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
          Ready to stop misinformation?
        </h2>

        {/* Supporting Text */}
        <p className="text-lg text-on-surface-variant max-w-2xl">
          Get the extension now and start verifying claims instantly. It's free, works on all major browsers, and respects your privacy.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <a
            href="https://chrome.google.com/webstore/category/extensions"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-lg font-semibold px-8 py-3 rounded-lg shadow-lg transition-colors"
          >
            <span className="material-symbols-outlined text-2xl">extension</span>
            <span>Get Extension</span>
          </a>
          <a
            href="/support"
            className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-on-surface text-lg font-medium px-8 py-3 rounded-lg transition-colors"
          >
            <span className="material-symbols-outlined text-2xl">help</span>
            <span>Learn More</span>
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
