'use client';

import { useState } from 'react';

type DemoResult = {
  verdict: string;
  verdictColor: string;
  confidence: string;
  summary: string;
  source1: string;
  source2: string;
};

export default function ClaimChecker() {
  const [claimText, setClaimText] = useState(
    "WHO declared synthetic vitamin D toxic to human bloodstreams in 2024."
  );
  const [result, setResult] = useState<DemoResult>({
    verdict: "UNCERTAIN",
    verdictColor: "tertiary",
    confidence: "61%",
    summary: "No official WHO decree matches this assertion, but ongoing regulatory evaluations regarding excessive synthetic megadoses create ambiguous colloquial reporting across news wires.",
    source1: "European Food Safety Authority (Oct 2024)",
    source2: "NIH Dietary Supplements Office (2024)"
  });

  const sampleClaims = [
    {
      text: "WHO declared synthetic vitamin D toxic to human bloodstreams in 2024.",
      verdict: "UNCERTAIN",
      verdictColor: "tertiary",
      confidence: "61%",
      summary: "No official WHO decree matches this assertion, but ongoing regulatory evaluations regarding excessive synthetic megadoses create ambiguous colloquial reporting across news wires.",
      source1: "European Food Safety Authority (Oct 2024)",
      source2: "NIH Dietary Supplements Office (2024)"
    },
    {
      text: "5G base stations induce acute viral respiratory infections.",
      verdict: "FAKE",
      verdictColor: "error",
      confidence: "94%",
      summary: "Physics of non-ionizing telecommunication bands fundamentally excludes cellular or pathogen mutation mechanics.",
      source1: "WHO Telecommunications Monograph",
      source2: "IEEE Electromagnetic Society"
    },
    {
      text: "Atmospheric carbon dioxide passed 420 ppm in verified Mauna Loa readings.",
      verdict: "REAL",
      verdictColor: "secondary",
      confidence: "97%",
      summary: "Multi-institutional observational tracking across NOAA and Scripps confirms steady annual progression over 420 ppm.",
      source1: "NOAA Global Monitoring Lab",
      source2: "Scripps Oceanography CO2 Program"
    }
  ];

  const handleQuickSample = (sample: DemoResult & { text: string }) => {
    setClaimText(sample.text);
    setResult({
      verdict: sample.verdict,
      verdictColor: sample.verdictColor,
      confidence: sample.confidence,
      summary: sample.summary,
      source1: sample.source1,
      source2: sample.source2
    });
  };

  return (
    <section className="py-8 flex flex-col gap-6">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          01 // Interactive Playground
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Check a claim in seconds.</h2>
        <p className="text-lg text-on-surface-variant">
          Paste a statement or explore structured evaluations generated through hybrid retrieval and citation cross-validation.
        </p>
      </div>

      {/* Playground Box */}
      <div className="bg-surface-container rounded-xl p-4 md:p-6 shadow-xl flex flex-col gap-6">
        {/* Input bar */}
        <div className="flex flex-col sm:flex-row items-stretch gap-2">
          <div className="flex-1 bg-surface-container-lowest rounded px-4 py-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-outline text-xl">search</span>
            <input
              className="bg-transparent border-none outline-none text-on-surface text-base w-full focus:ring-0 placeholder:text-outline"
              placeholder="Paste any headline, quote, or claim..."
              type="text"
              value={claimText}
              onChange={(e) => setClaimText(e.target.value)}
            />
          </div>
          <button className="bg-primary-container hover:bg-surface-tint text-on-primary-fixed text-base font-semibold px-6 py-2.5 rounded transition-colors flex items-center justify-center gap-2 shrink-0">
            <span className="material-symbols-outlined text-lg">neurology</span>
            <span>Check claim</span>
          </button>
        </div>

        {/* Presets / Toggles */}
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <span className="text-outline text-xs uppercase">Quick samples:</span>
          {sampleClaims.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => handleQuickSample(sample)}
              className="px-3 py-1 rounded bg-surface-container-high hover:bg-surface-container-highest text-on-surface transition-colors font-mono text-xs"
            >
              Try: {sample.text.split('.')[0].substring(0, 30)}...
            </button>
          ))}
        </div>

        {/* Active Loaded Verification Result */}
        <div className="bg-surface-container-low rounded p-4 md:p-6 flex flex-col gap-4">
          {/* Status Row */}
          <div className="flex flex-wrap items-center justify-between gap-2 pb-2">
            <div className="flex items-center gap-4">
              <span className={`text-sm font-semibold px-2.5 py-1 rounded tracking-wide bg-${result.verdictColor}-container/20 text-${result.verdictColor}`}>
                VERDICT: {result.verdict}
              </span>
              <span className="text-sm text-on-surface-variant font-mono">
                CONFIDENCE: {result.confidence}
              </span>
            </div>
            <span className="text-xs text-outline">LATENCY: 182ms • HYBRID BM25+EMBED</span>
          </div>

          {/* Assessment Paragraph */}
          <div className="flex flex-col gap-1">
            <span className="text-xs text-outline uppercase tracking-wider">Synthesized Assessment</span>
            <p className="text-base text-on-surface leading-relaxed">
              {result.summary}
            </p>
          </div>

          {/* Evidentiary Sub-Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="bg-surface-container p-4 rounded flex flex-col justify-between gap-2">
              <div className="flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-secondary font-mono">{result.source1}</span>
                  <span className="material-symbols-outlined text-base text-outline">open_in_new</span>
                </div>
                <p className="text-sm text-on-surface-variant">
                  "Tolerable Upper Intake Levels for Vitamin D reaffirmed; no systemic bloodstream toxicity detected under standard therapeutic guidelines."
                </p>
              </div>
              <div className="flex items-center justify-between text-xs text-outline pt-2">
                <span>Primary Regulatory Dossier</span>
                <span className="text-on-surface font-mono">Strength: 91%</span>
              </div>
            </div>
            
            <div className="bg-surface-container p-4 rounded flex flex-col justify-between gap-2">
              <div className="flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-secondary font-mono">{result.source2}</span>
                  <span className="material-symbols-outlined text-base text-outline">open_in_new</span>
                </div>
                <p className="text-sm text-on-surface-variant">
                  "Hypercalcemia risks are limited to hyper-megadose cases (&gt;50,000 IU/day over prolonged intervals). No broad categorization of toxicity exists."
                </p>
              </div>
              <div className="flex items-center justify-between text-xs text-outline pt-2">
                <span>Biomedical Consensus</span>
                <span className="text-on-surface font-mono">Strength: 86%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
