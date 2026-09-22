'use client';

import { useEffect } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';

// Simple privacy-friendly analytics
// Replace with your preferred service: Plausible, Fathom, Simple Analytics
export default function Analytics() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    // Track page views
    const url = `${pathname}${searchParams.toString() ? `?${searchParams.toString()}` : ''}`;
    
    // Example: Send to your analytics endpoint
    // fetch('/api/analytics', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //     event: 'pageview',
    //     url,
    //     referrer: document.referrer,
    //     timestamp: new Date().toISOString(),
    //   }),
    // });

    // Example: Plausible Analytics (privacy-friendly, GDPR compliant)
    // if (window.plausible) {
    //   window.plausible('pageview');
    // }
    
    console.log('Page view:', url);
  }, [pathname, searchParams]);

  return null;
}

// Add this to your layout.tsx if you want to use Plausible:
// <script defer data-domain="your-domain.com" src="https://plausible.io/js/script.js"></script>
