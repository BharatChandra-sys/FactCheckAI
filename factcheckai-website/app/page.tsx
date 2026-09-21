import Header from '@/components/Header';
import Footer from '@/components/Footer';
import HeroSection from '@/components/HeroSection';
import TrustStrip from '@/components/TrustStrip';
import ClaimChecker from '@/components/ClaimChecker';
import HowItWorks from '@/components/HowItWorks';
import EvidenceSection from '@/components/EvidenceSection';
import TechnologySection from '@/components/TechnologySection';
import BrowserExtension from '@/components/BrowserExtension';
import UncertaintySection from '@/components/UncertaintySection';
import TransparencySection from '@/components/TransparencySection';
import OpenSourceSection from '@/components/OpenSourceSection';
import FAQSection from '@/components/FAQSection';
import CTASection from '@/components/CTASection';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-surface">
      <Header />
      
      <main className="w-full pt-16 bg-surface max-w-7xl mx-auto px-4 md:px-8 lg:px-12 flex-1">
        <div className="flex flex-col w-full">
          <HeroSection />
          <TrustStrip />
          <ClaimChecker />
          <HowItWorks />
          <EvidenceSection />
          <TechnologySection />
          <BrowserExtension />
          <UncertaintySection />
          <TransparencySection />
          <OpenSourceSection />
          <FAQSection />
          <CTASection />
        </div>
      </main>

      <Footer />
    </div>
  );
}
