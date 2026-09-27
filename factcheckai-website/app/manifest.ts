import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'TruvantaAI - AI-Powered Fact Verification',
    short_name: 'TruvantaAI',
    description: 'Professional AI-assisted fact verification. Real-time fake news detection powered by hybrid retrieval and evidence-based reasoning.',
    start_url: '/',
    display: 'standalone',
    background_color: '#101419',
    theme_color: '#c0c1ff',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  };
}
