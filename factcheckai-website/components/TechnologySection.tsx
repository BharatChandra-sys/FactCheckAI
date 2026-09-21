export default function TechnologySection() {
  const techComponents = [
    { icon: "psychology", label: "RoBERTa-Large", sublabel: "Stance Detection" },
    { icon: "hub", label: "Hybrid RAG", sublabel: "BM25 + Dense" },
    { icon: "function", label: "MiniLM-L6", sublabel: "Embeddings" },
    { icon: "storage", label: "pgvector", sublabel: "HNSW Index" },
    { icon: "schema", label: "Reciprocal Rank", sublabel: "Fusion Algorithm" },
    { icon: "batch_prediction", label: "Ensemble Voting", sublabel: "Multi-Model" },
    { icon: "network_check", label: "Citation Graph", sublabel: "Link Analysis" },
    { icon: "troubleshoot", label: "Calibration", sublabel: "Uncertainty Est." }
  ];

  return (
    <section className="py-8 flex flex-col gap-8" id="technology">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          04 // Technical Stack
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Built on open-source AI research</h2>
        <p className="text-lg text-on-surface-variant">
          Transparent, reproducible, and peer-reviewed architectures power every component—no black-box magic.
        </p>
      </div>

      {/* Tech Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {techComponents.map((tech, idx) => (
          <div
            key={idx}
            className="bg-surface-container p-4 rounded-lg flex flex-col items-center gap-3 hover:bg-surface-container-high transition-colors text-center"
          >
            <span className="material-symbols-outlined text-3xl text-surface-tint">
              {tech.icon}
            </span>
            <div className="flex flex-col gap-0.5">
              <span className="text-sm font-semibold text-on-surface">{tech.label}</span>
              <span className="text-xs text-on-surface-variant">{tech.sublabel}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Tech Details */}
      <div className="bg-surface-container-low p-6 rounded-xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div className="flex flex-col gap-2">
            <span className="text-xs uppercase tracking-wider text-surface-tint font-mono">Language Models</span>
            <p className="text-on-surface-variant leading-relaxed">
              Fine-tuned transformer models (RoBERTa, BERT) specialized for stance detection, claim decomposition, and bias identification.
            </p>
          </div>
          <div className="flex flex-col gap-2">
            <span className="text-xs uppercase tracking-wider text-secondary font-mono">Retrieval Architecture</span>
            <p className="text-on-surface-variant leading-relaxed">
              Hybrid BM25 + dense vector search with reciprocal rank fusion ensures both keyword precision and semantic recall.
            </p>
          </div>
          <div className="flex flex-col gap-2">
            <span className="text-xs uppercase tracking-wider text-tertiary font-mono">Uncertainty Quantification</span>
            <p className="text-on-surface-variant leading-relaxed">
              Probabilistic calibration using temperature scaling and ensemble disagreement metrics to surface epistemic uncertainty.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
