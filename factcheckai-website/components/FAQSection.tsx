'use client';

import { useState } from 'react';

export default function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      question: "How does FactCheckAI differ from other fact-checkers?",
      answer: "Unlike binary fact-checkers, we surface uncertainty when evidence is ambiguous. We use hybrid ML+retrieval instead of purely manual fact-checking, and we provide full transparency with source citations and confidence calibration."
    },
    {
      question: "What data do you collect from users?",
      answer: "Zero. FactCheckAI operates entirely client-side for claim extraction. Evidence retrieval happens on our backend, but we never log queries, user identities, or browsing history. See our privacy policy for full details."
    },
    {
      question: "Can I use FactCheckAI for academic research?",
      answer: "Absolutely. All models, datasets, and evaluation scripts are open-source under MIT license. Cite our research papers (linked in GitHub repo) and feel free to extend or fork the project."
    },
    {
      question: "Which browsers are supported?",
      answer: "Chrome, Edge, Firefox, and Brave. The extension is available on Chrome Web Store and Firefox Add-ons. Safari support is planned for 2025."
    },
    {
      question: "How accurate are the verdicts?",
      answer: "On our held-out test set, we achieve 89% accuracy for binary classification (Real/Fake) and 76% for three-way (Real/Uncertain/Fake). Confidence scores are calibrated to within ±3% expected calibration error."
    },
    {
      question: "Can I contribute to improving the models?",
      answer: "Yes! We welcome contributions: bug reports, dataset suggestions, model improvements, and UI feedback. Check our GitHub repo's CONTRIBUTING.md for guidelines."
    }
  ];

  return (
    <section className="py-8 flex flex-col gap-8">
      <div className="flex flex-col gap-2 max-w-2xl">
        <span className="text-sm uppercase tracking-widest text-surface-tint font-mono">
          09 // Frequently Asked
        </span>
        <h2 className="text-4xl font-bold text-on-surface">Questions & Answers</h2>
        <p className="text-lg text-on-surface-variant">
          Common queries about how FactCheckAI works, privacy, accuracy, and contribution guidelines.
        </p>
      </div>

      {/* Accordion */}
      <div className="flex flex-col gap-3">
        {faqs.map((faq, index) => (
          <div
            key={index}
            className="bg-surface-container rounded-xl overflow-hidden hover:bg-surface-container-high transition-colors"
          >
            <button
              onClick={() => setOpenIndex(openIndex === index ? null : index)}
              className="w-full px-6 py-4 flex items-center justify-between gap-4 text-left"
            >
              <span className="text-base font-semibold text-on-surface">{faq.question}</span>
              <span className={`material-symbols-outlined text-2xl text-surface-tint transition-transform ${openIndex === index ? 'rotate-180' : ''}`}>
                expand_more
              </span>
            </button>
            {openIndex === index && (
              <div className="px-6 pb-4 pt-0">
                <p className="text-sm text-on-surface-variant leading-relaxed">
                  {faq.answer}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
