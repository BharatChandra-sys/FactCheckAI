export default function TransparencySection() {
  const auditTrail = [
    {
      step: "1",
      title: "Claim Ingestion",
      detail: "User-selected text captured with full context",
      timestamp: "t=0ms"
    },
    {
      step: "2",
      title: "ML Classification",
      detail: "RoBERTa stance model: 0.87 fake probability",
      timestamp: "t=42ms"
    },
    {
      step: "3",
      title: "Evidence Retrieval",
      detail: "23 sources retrieved via hybrid BM25+vector",
      timestamp: "t=128ms"
    },
    {
      step: "4",
      title: "Citation Validation",
      detail: "3 sources verified, 2 contradictory dismissed",
      timestamp: "t=165ms"
    },
    {
      step: "5",
      title: "Uncertainty Calibration",
      detail: "Final confidence: 87.4% (calibrated)",
      timestamp: "t=182ms"
    }
  ];

  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          07 // Transparency
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Every verdict comes with receipts</h2>
        <p className="text-lg text-on-surface-variant">
          Full audit trails show exactly which sources were consulted, how confidence was calculated, and which reasoning chain produced the final verdict.
        </p>
      </div>

      {/* Audit Trail Timeline */}
      <div className="bg-surface-container rounded-xl p-6">
        <div className="relative">
          {/* Vertical Line */}
          <div className="absolute left-4 top-8 bottom-8 w-0.5 bg-outline-variant"></div>

          {/* Timeline Steps */}
          <div className="space-y-6">
            {auditTrail.map((item) => (
              <div key={item.step} className="relative flex gap-4">
                {/* Step Number Bubble */}
                <div className="relative z-10 flex items-center justify-center w-8 h-8 rounded-full bg-surface-tint text-surface font-bold text-sm shrink-0">
                  {item.step}
                </div>

                {/* Step Content */}
                <div className="flex-1 bg-surface-container-low p-4 rounded-lg">
                  <div className="flex items-start justify-between gap-4 mb-1">
                    <h4 className="text-base font-semibold text-on-surface">{item.title}</h4>
                    <span className="text-xs text-on-surface-variant font-mono shrink-0">{item.timestamp}</span>
                  </div>
                  <p className="text-sm text-on-surface-variant">{item.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Transparency Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-surface-tint">article</span>
          <h4 className="text-lg font-semibold text-on-surface">Full Source Citations</h4>
          <p className="text-sm text-on-surface-variant">
            Every verdict includes clickable citations to original source documents with relevance scores.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-secondary">data_object</span>
          <h4 className="text-lg font-semibold text-on-surface">Reasoning Chain Export</h4>
          <p className="text-sm text-on-surface-variant">
            Download complete JSON logs of model inputs, retrieval results, and decision logic.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <span className="material-symbols-outlined text-2xl text-tertiary">thumbs_up_down</span>
          <h4 className="text-lg font-semibold text-on-surface">User Feedback Loop</h4>
          <p className="text-sm text-on-surface-variant">
            Report incorrect verdicts to improve models. All feedback is human-reviewed and transparent.
          </p>
        </div>
      </div>
    </section>
  );
}
