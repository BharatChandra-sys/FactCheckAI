export default function TrustStrip() {
  return (
    <section className="py-4 my-6 bg-surface-container-low">
      <div className="flex flex-wrap items-center justify-between gap-y-2 gap-x-4 text-on-surface-variant text-sm uppercase tracking-wider">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-lg text-surface-tint">memory</span>
          <span>ML Classification</span>
        </div>
        <span className="text-outline-variant hidden md:inline">•</span>
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-lg text-secondary">database</span>
          <span>Evidence Retrieval</span>
        </div>
        <span className="text-outline-variant hidden md:inline">•</span>
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-lg text-tertiary">schema</span>
          <span>RAG Reasoning</span>
        </div>
        <span className="text-outline-variant hidden md:inline">•</span>
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-lg text-surface-tint">menu_book</span>
          <span>Citation Validation</span>
        </div>
        <span className="text-outline-variant hidden md:inline">•</span>
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-lg text-error">troubleshoot</span>
          <span>Uncertainty Detection</span>
        </div>
      </div>
    </section>
  );
}
