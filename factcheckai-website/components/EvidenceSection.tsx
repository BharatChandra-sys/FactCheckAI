export default function EvidenceSection() {
  const evidenceSources = [
    {
      icon: "science",
      title: "Peer-Reviewed Studies",
      description: "Cross-referenced from PubMed, arXiv, IEEE Xplore, and institutional repositories.",
      metrics: "4.2M+ Articles",
      color: "surface-tint"
    },
    {
      icon: "newspaper",
      title: "Accredited News Wires",
      description: "Vetted journalism from Reuters, AP, BBC, and fact-check consortiums like Poynter IFCN.",
      metrics: "1.8M+ Archives",
      color: "secondary"
    },
    {
      icon: "account_balance",
      title: "Government & NGO Data",
      description: "Primary data from WHO, CDC, NOAA, EPA, and UN specialized agencies.",
      metrics: "890K+ Records",
      color: "tertiary"
    }
  ];

  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div className="flex flex-col gap-2 max-w-2xl">
          <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
            03 // Primary Sources
          </span>
          <h2 className="text-4xl font-bold text-on-surface">Evidence from trusted institutions</h2>
          <p className="text-lg text-on-surface-variant">
            Our hybrid retrieval engine queries over 7 million documents, ensuring every verdict is grounded in verifiable, authoritative sources.
          </p>
        </div>
      </div>

      {/* Evidence Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {evidenceSources.map((source, idx) => (
          <div
            key={idx}
            className="bg-surface-container p-6 rounded-xl flex flex-col gap-4 hover:bg-surface-container-high transition-colors shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className={`material-symbols-outlined text-3xl text-${source.color}`}>
                {source.icon}
              </span>
              <span className={`text-sm font-mono text-${source.color} bg-${source.color}/10 px-2 py-1 rounded`}>
                {source.metrics}
              </span>
            </div>
            <h3 className="text-xl font-semibold text-on-surface">{source.title}</h3>
            <p className="text-base text-on-surface-variant leading-relaxed">
              {source.description}
            </p>
            <div className="flex items-center gap-2 text-sm text-on-surface-variant pt-2">
              <span className="material-symbols-outlined text-base text-secondary">verified</span>
              <span>Continuously Updated</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
