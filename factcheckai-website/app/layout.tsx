import type { Metadata } from "next";
import { Space_Grotesk, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({ 
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  weight: ['400', '500', '600', '700'],
  display: 'swap',
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-ibm-plex-mono",
  weight: ['400', '500', '600'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: "FactCheckAI - Verify what you read, before you believe it",
  description: "Professional AI-assisted fact verification. Real-time fake news detection powered by hybrid retrieval and evidence-based reasoning.",
  keywords: ["fact-checking", "AI", "misinformation", "fake news", "browser extension"],
  authors: [{ name: "FactCheckAI Team", url: "https://gari.live" }],
  creator: "FactCheckAI",
  publisher: "FactCheckAI",
  openGraph: {
    title: "FactCheckAI - AI-Powered Fact Verification",
    description: "Verify claims instantly with our professional browser extension. Evidence-based fact-checking at your fingertips.",
    type: "website",
    url: "https://factcheckai.vercel.app",
  },
  twitter: {
    card: "summary_large_image",
    title: "FactCheckAI - AI-Powered Fact Verification",
    description: "Professional fact-checking extension",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
          rel="stylesheet"
        />
      </head>
      <body className={`${spaceGrotesk.variable} ${ibmPlexMono.variable} font-sans antialiased min-h-screen bg-background text-on-surface`}>
        {children}
      </body>
    </html>
  );
}
