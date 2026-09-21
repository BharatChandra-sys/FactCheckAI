export default function UncertaintySection() {
  const verdicts = [
    {
      label: "REAL",
      color: "secondary",
      bgColor: "bg-secondary/10",
      textColor: "text-secondary",
      confidence: "92-100%",
      description: "Strong consensus across multiple high-authority sources with no conflicting evidence.",
      icon: "check_circle"
    },
    {
      label: "UNCERTAIN",
      color: "tertiary",
      bgColor: "bg-tertiary/10",
      textColor: "text-tertiary",
      confidence: "45-75%",
      description: "Conflicting evidence, ambiguous framing, or insufficient authoritative coverage.",
      icon: "help"
    },
    {
      label: "FAKE",
      color: "error",
      bgColor: "bg-error/10",
      textColor: "text-error",
      confidence: "85-100%",
      description: "Direct contradiction by multiple credible sources with strong empirical refutation.",
      icon: "cancel"
    }
  ];

  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          06 // Verdict System
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Honest about what we don't know</h2>
        <p className="text-lg text-on-surface-variant">
          Unlike binary fact-checkers, FactCheckAI surfaces uncertainty when evidence is conflicting or insufficient. Confidence scores are calibrated to reflect epistemic limitations.
        </p>
      </div>

      {/* Verdict Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {verdicts.map((verdict) => (
          <div
            key={verdict.label}
            className={`${verdict.bgColor} p-6 rounded-xl flex flex-col gap-4 hover:bg-opacity-20 transition-all shadow-md`}
          >
            <div className="flex items-center justify-between">
              <span className={`material-symbols-outlined text-3xl ${verdict.textColor}`}>
                {verdict.icon}
              </span>
              <span className={`text-xs font-mono ${verdict.textColor} bg-${verdict.color}/20 px-2 py-1 rounded`}>
                {verdict.confidence}
              </span>
            </div>
            <h3 className={`text-2xl font-bold ${verdict.textColor} uppercase tracking-wide`}>
              {verdict.label}
            </h3>
            <p className="text-sm text-on-surface-variant leading-relaxed">
              {verdict.description}
            </p>
            <div className="flex items-center gap-2 text-xs text-on-surface-variant pt-2">
              <span className="material-symbols-outlined text-sm">info</span>
              <span>Calibrated via temperature scaling</span>
            </div>
          </div>
        ))}
      </div>

      {/* Calibration Explanation */}
      <div className="bg-surface-container p-6 rounded-xl">
        <div className="flex flex-col md:flex-row gap-6 items-start">
          <div className="flex-1">
            <h4 className="text-lg font-semibold text-on-surface mb-2">Calibrated Confidence</h4>
            <p className="text-sm text-on-surface-variant leading-relaxed">
              Our models undergo post-hoc calibration to ensure confidence scores accurately reflect true prediction accuracy. When we say 90% confidence, we're right ~90% of the time—not inflating certainty to seem more authoritative.
            </p>
          </div>
          <div className="flex-1">
            <h4 className="text-lg font-semibold text-on-surface mb-2">Epistemic Humility</h4>
            <p className="text-sm text-on-surface-variant leading-relaxed">
              Emerging claims, niche scientific debates, or politically contested topics often lack clear consensus. We flag these as UNCERTAIN rather than forcing a binary verdict—honoring the complexity of real-world information.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
