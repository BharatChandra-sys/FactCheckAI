export default function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-surface">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-surface-container-high border-t-surface-tint mb-4"></div>
        <p className="text-on-surface-variant text-sm">Loading...</p>
      </div>
    </div>
  );
}
