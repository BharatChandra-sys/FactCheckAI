export default function OpenSourceSection() {
  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          08 // Community
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Built with transparency, powered by community</h2>
        <p className="text-lg text-on-surface-variant">
          Every model, algorithm, and data pipeline is openly documented. Community contributions drive continuous improvement.
        </p>
      </div>

      {/* GitHub Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-surface-container p-6 rounded-xl flex flex-col gap-2 text-center">
          <span className="material-symbols-outlined text-3xl text-tertiary mx-auto">star</span>
          <span className="text-3xl font-bold text-on-surface">1.8k</span>
          <span className="text-sm text-on-surface-variant">GitHub Stars</span>
        </div>
        <div className="bg-surface-container p-6 rounded-xl flex flex-col gap-2 text-center">
          <span className="material-symbols-outlined text-3xl text-surface-tint mx-auto">code</span>
          <span className="text-3xl font-bold text-on-surface">342</span>
          <span className="text-sm text-on-surface-variant">Contributors</span>
        </div>
        <div className="bg-surface-container p-6 rounded-xl flex flex-col gap-2 text-center">
          <span className="material-symbols-outlined text-3xl text-secondary mx-auto">merge</span>
          <span className="text-3xl font-bold text-on-surface">1.2k</span>
          <span className="text-sm text-on-surface-variant">Pull Requests</span>
        </div>
        <div className="bg-surface-container p-6 rounded-xl flex flex-col gap-2 text-center">
          <span className="material-symbols-outlined text-3xl text-error mx-auto">verified</span>
          <span className="text-3xl font-bold text-on-surface">MIT</span>
          <span className="text-sm text-on-surface-variant">License</span>
        </div>
      </div>

      {/* CTA Block */}
      <div className="bg-surface-container-low p-8 rounded-xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex-1">
          <h3 className="text-2xl font-bold text-on-surface mb-2">Join the community</h3>
          <p className="text-base text-on-surface-variant">
            Contribute to models, suggest features, or help improve documentation. All skill levels welcome.
          </p>
        </div>
        <div className="flex flex-wrap gap-3 shrink-0">
          <a
            href="https://github.com/yourusername/factcheckai"
            target="_blank"
            className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-on-surface text-sm font-medium px-4 py-2 rounded transition-colors"
          >
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            View Repository
          </a>
          <a
            href="https://github.com/yourusername/factcheckai/blob/main/CONTRIBUTING.md"
            target="_blank"
            className="inline-flex items-center gap-2 bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-sm font-semibold px-4 py-2 rounded transition-colors"
          >
            <span className="material-symbols-outlined text-lg">groups</span>
            Contribute
          </a>
        </div>
      </div>
    </section>
  );
}
