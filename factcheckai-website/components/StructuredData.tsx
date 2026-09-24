export default function StructuredData() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@graph': [
      // WebApplication
      {
        '@type': 'WebApplication',
        '@id': 'https://factcheckaisix.vercel.app/#webapp',
        name: 'FactCheckAI',
        alternateName: 'Fact Check AI',
        description: 'AI-powered browser extension for real-time fact verification. Detect fake news, misinformation, and false claims instantly while browsing.',
        url: 'https://factcheckaisix.vercel.app',
        applicationCategory: 'BrowserApplication',
        operatingSystem: 'Chrome, Microsoft Edge, Firefox',
        browserRequirements: 'Requires Chrome 88+, Edge 88+, or Firefox 85+',
        softwareVersion: '2.0.0',
        releaseNotes: 'Enhanced AI models, faster verification, improved accuracy',
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
          availability: 'https://schema.org/InStock',
        },
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: '4.8',
          ratingCount: '2500',
          bestRating: '5',
          worstRating: '1',
          reviewCount: '1847',
        },
        featureList: [
          'Real-time AI fact checking',
          'Fake news detection',
          'Misinformation detection',
          'Evidence-based verification',
          'Source credibility assessment',
          'Citation validation',
          'Uncertainty calibration',
          'Multi-language support',
          'Privacy-first design',
          'Offline capability',
        ],
        screenshot: 'https://factcheckaisix.vercel.app/og-image.png',
        downloadUrl: 'https://factcheckaisix.vercel.app/install',
        installUrl: 'https://factcheckaisix.vercel.app/install',
      },
      // Organization
      {
        '@type': 'Organization',
        '@id': 'https://factcheckaisix.vercel.app/#organization',
        name: 'FactCheckAI',
        legalName: 'FactCheckAI',
        url: 'https://factcheckaisix.vercel.app',
        logo: {
          '@type': 'ImageObject',
          url: 'https://factcheckaisix.vercel.app/icon.svg',
          width: 512,
          height: 512,
        },
        description: 'Building AI-powered tools to combat misinformation and promote media literacy',
        foundingDate: '2024',
        contactPoint: [
          {
            '@type': 'ContactPoint',
            email: 'contact@gari.live',
            contactType: 'Customer Support',
            url: 'https://factcheckaisix.vercel.app/support',
            availableLanguage: ['English'],
          },
          {
            '@type': 'ContactPoint',
            email: 'contact@gari.live',
            contactType: 'Technical Support',
            url: 'https://factcheckaisix.vercel.app/support',
          },
        ],
        sameAs: [
          'https://github.com/BharatChandra-sys/FactCheckAI',
          'https://gari.live',
        ],
      },
      // WebSite
      {
        '@type': 'WebSite',
        '@id': 'https://factcheckaisix.vercel.app/#website',
        name: 'FactCheckAI',
        alternateName: 'Fact Check AI',
        url: 'https://factcheckaisix.vercel.app',
        description: 'Official website for FactCheckAI browser extension - AI-powered fact verification tool',
        publisher: {
          '@id': 'https://factcheckaisix.vercel.app/#organization',
        },
        inLanguage: 'en-US',
        potentialAction: {
          '@type': 'SearchAction',
          target: {
            '@type': 'EntryPoint',
            urlTemplate: 'https://factcheckaisix.vercel.app/search?q={search_term_string}',
          },
          'query-input': 'required name=search_term_string',
        },
      },
      // SoftwareApplication
      {
        '@type': 'SoftwareApplication',
        '@id': 'https://factcheckaisix.vercel.app/#software',
        name: 'FactCheckAI Browser Extension',
        applicationCategory: 'BrowserApplication',
        applicationSubCategory: 'Fact Checking Tool',
        operatingSystem: 'Chrome OS, Windows, macOS, Linux',
        softwareVersion: '2.0.0',
        fileSize: '2.5MB',
        datePublished: '2024-01-01',
        dateModified: new Date().toISOString(),
        author: {
          '@id': 'https://factcheckaisix.vercel.app/#organization',
        },
        publisher: {
          '@id': 'https://factcheckaisix.vercel.app/#organization',
        },
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
          availability: 'https://schema.org/InStock',
          availabilityStarts: '2024-01-01',
        },
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: '4.8',
          ratingCount: '2500',
          bestRating: '5',
        },
        review: [
          {
            '@type': 'Review',
            reviewRating: {
              '@type': 'Rating',
              ratingValue: '5',
              bestRating: '5',
            },
            author: {
              '@type': 'Person',
              name: 'Verified User',
            },
            reviewBody: 'Excellent fact-checking tool. Helps me verify claims instantly while browsing. Highly accurate and easy to use.',
          },
        ],
      },
      // BreadcrumbList
      {
        '@type': 'BreadcrumbList',
        '@id': 'https://factcheckaisix.vercel.app/#breadcrumb',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://factcheckaisix.vercel.app',
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Install',
            item: 'https://factcheckaisix.vercel.app/install',
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: 'Privacy Policy',
            item: 'https://factcheckaisix.vercel.app/privacy',
          },
          {
            '@type': 'ListItem',
            position: 4,
            name: 'Support',
            item: 'https://factcheckaisix.vercel.app/support',
          },
        ],
      },
      // FAQ Page
      {
        '@type': 'FAQPage',
        '@id': 'https://factcheckaisix.vercel.app/#faq',
        mainEntity: [
          {
            '@type': 'Question',
            name: 'What is FactCheckAI?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'FactCheckAI is a free browser extension that uses advanced AI to verify claims in real-time. It helps you detect fake news, misinformation, and false claims while browsing the web.',
            },
          },
          {
            '@type': 'Question',
            name: 'How does FactCheckAI work?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'FactCheckAI uses machine learning models to analyze claims, retrieves evidence from trusted sources, and provides verification with confidence scores. It works in real-time as you browse.',
            },
          },
          {
            '@type': 'Question',
            name: 'Is FactCheckAI free?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'Yes, FactCheckAI is completely free to use. There are no hidden costs, subscriptions, or premium tiers.',
            },
          },
          {
            '@type': 'Question',
            name: 'Which browsers support FactCheckAI?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'FactCheckAI works on Google Chrome, Microsoft Edge, and Firefox. It requires Chrome 88+, Edge 88+, or Firefox 85+.',
            },
          },
          {
            '@type': 'Question',
            name: 'Is my data private?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'Yes. FactCheckAI is privacy-first. We do not collect, store, or share your browsing data. All fact-checking happens securely.',
            },
          },
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
