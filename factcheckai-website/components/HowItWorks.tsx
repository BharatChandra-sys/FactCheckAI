export default function HowItWorks() {
  const steps = [
    {
      number: "01",
      label: "INGESTION",
      icon: "select_all",
      color: "surface-tint",
      title: "Claim Extraction",
      description: "The user selects text from any live webpage or submits a raw string. The local client isolates entity boundaries and context sentences.",
      output: "INPUT: DOM Span / UTF-8"
    },
    {
      number: "02",
      label: "NLP DECOMPOSITION",
      icon: "model_training",
      color: "secondary",
      title: "ML Analysis",
      description: "Fine-tuned RoBERTa models evaluate linguistic markers, sensationalist bias, emotional appeal, and decompose compound claims into atomic assertions.",
      output: "PREMISE: Stance + Polarity"
    },
    {
      number: "03",
      label: "RETRIEVAL",
      icon: "hub",
      color: "tertiary",
      title: "Evidence + RAG",
      description: "Reciprocal Rank Fusion simultaneously queries BM25 indices and dense pgvector embeddings over millions of peer-reviewed articles and accredited news wires.",
      output: "VECTOR: HNSW + MiniLM-L6"
    },
    {
      number: "04",
      label: "SYNTHESIS",
      icon: "verified",
      color: "error",
      title: "Final Assessment",
      description: "Evidence signals are synthesized with chain-of-thought verification. Uncertainty is calibrated and output alongside verifiable source citations.",
      output: "OUTPUT: Calibrated Verdict"
    }
  ];

  return (
    <section className="py-8 flex flex-col gap-8" id="how-it-works">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          02 // Pipeline Architecture
        </span>
        <h2 className="text-4xl font-bold text-on-surface">How FactCheckAI verifies information</h2>
        <p className="text-lg text-on-surface-variant">
          Every evaluation traverses a 4-step forensic verification loop designed to prevent hallucinations and establish an immutable chain of custody for sources.
        </p>
      </div>

      {/* 4 Interconnected Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 relative">
        {steps.map((step) => (
          <div
            key={step.number}
            className="bg-surface-container p-6 rounded-xl flex flex-col justify-between gap-6 shadow-md hover:bg-surface-container-high transition-colors"
          >
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <span className={`text-xs px-2 py-1 rounded bg-surface-container-highest text-${step.color} font-mono`}>
                  {step.number} // {step.label}
                </span>
                <span className="material-symbols-outlined text-outline text-2xl">{step.icon}</span>
              </div>
              <h3 className="text-lg font-semibold text-on-surface">{step.title}</h3>
              <p className="text-sm text-on-surface-variant leading-relaxed">
                {step.description}
              </p>
            </div>
            <div className="text-xs text-outline font-mono">
              {step.output}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
