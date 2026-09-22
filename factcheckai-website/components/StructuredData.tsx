export default function StructuredData() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebApplication',
        name: 'FactCheckAI',
        description: 'Professional AI-assisted fact verification browser extension',
        applicationCategory: 'BrowserApplication',
        operatingSystem: 'Chrome, Edge, Firefox',
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
        },
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: '4.8',
          ratingCount: '1847',
          bestRating: '5',
          worstRating: '1',
        },
      },
      {
        '@type': 'Organization',
        name: 'FactCheckAI',
        url: 'https://factcheckai.vercel.app',
        contactPoint: {
          '@type': 'ContactPoint',
          email: 'contact@gari.live',
          contactType: 'Customer Support',
          url: 'https://factcheckai.vercel.app/support',
        },
        sameAs: [
          'https://gari.live',
        ],
      },
      {
        '@type': 'WebSite',
        name: 'FactCheckAI',
        url: 'https://factcheckai.vercel.app',
        potentialAction: {
          '@type': 'SearchAction',
          target: {
            '@type': 'EntryPoint',
            urlTemplate: 'https://factcheckai.vercel.app/?q={search_term_string}',
          },
          'query-input': 'required name=search_term_string',
        },
      },
      {
        '@type': 'SoftwareApplication',
        name: 'FactCheckAI Browser Extension',
        operatingSystem: 'Chrome, Edge, Firefox',
        applicationCategory: 'BrowserApplication',
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
        },
        featureList: [
          'Real-time fact checking',
          'AI-powered verification',
          'Evidence retrieval',
          'Citation tracking',
          'Uncertainty calibration',
        ],
      },
    ],
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  );
}
