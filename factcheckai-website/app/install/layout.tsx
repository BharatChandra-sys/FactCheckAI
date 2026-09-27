import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Installation Guide',
  description: 'Step-by-step guide to install TruvantaAI browser extension on Chrome and Edge.',
  alternates: {
    canonical: 'https://truvantaai.tech/install',
  },
};

export default function InstallLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
