import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: "FactCheckAI - Verify what you read, before you believe it",
  description: "Open-source AI-assisted fact verification. Real-time fake news detection powered by hybrid retrieval and evidence-based reasoning.",
  keywords: ["fact-checking", "AI", "misinformation", "fake news", "browser extension", "open source"],
  authors: [{ name: "FactCheckAI Team" }],
  openGraph: {
    title: "FactCheckAI - AI-Powered Fact Verification",
    description: "Verify claims instantly with our open-source browser extension. Evidence-based fact-checking at your fingertips.",
    type: "website",
    url: "https://factcheckai.vercel.app",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
          rel="stylesheet"
        />
      </head>
      <body className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased min-h-screen bg-background text-on-surface`}>
        {children}
      </body>
    </html>
  );
}
