'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function InstallGuidePage() {
  const steps = [
    {
      number: 1,
      title: 'Download the Extension',
      description: 'Click the button below to download the FactCheckAI extension ZIP file.',
      action: (
        <motion.a
          href="/factcheckai-extension.zip"
          download
          className="inline-flex items-center gap-2 bg-brand-yellow hover:bg-brand-orange text-black text-base font-semibold px-6 py-3 rounded transition-colors shadow-lg"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <span className="material-symbols-outlined text-xl">download</span>
          <span>Download Extension</span>
        </motion.a>
      ),
      image: (
        <div className="bg-surface-container rounded-lg p-8 border border-brand-yellow/30">
          <div className="flex flex-col items-center gap-4">
            <span className="material-symbols-outlined text-6xl text-brand-yellow">folder_zip</span>
            <span className="text-sm text-on-surface-variant font-mono">factcheckai-extension.zip</span>
          </div>
        </div>
      )
    },
    {
      number: 2,
      title: 'Extract the ZIP File',
      description: 'Right-click the downloaded file and select "Extract All" or use your preferred extraction tool.',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-outline-variant/30">
          <div className="space-y-3">
            <div className="flex items-center gap-3 bg-surface-container-low p-3 rounded">
              <span className="material-symbols-outlined text-brand-yellow">folder_zip</span>
              <span className="text-sm">factcheckai-extension.zip</span>
            </div>
            <div className="flex justify-center">
              <span className="material-symbols-outlined text-2xl text-on-surface-variant">arrow_downward</span>
            </div>
            <div className="flex items-center gap-3 bg-surface-container-low p-3 rounded">
              <span className="material-symbols-outlined text-secondary">folder_open</span>
              <span className="text-sm">factcheckai-extension/</span>
            </div>
          </div>
        </div>
      )
    },
    {
      number: 3,
      title: 'Open Chrome Extensions',
      description: 'Open Chrome/Edge and navigate to chrome://extensions or edge://extensions',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-outline-variant/30">
          <div className="space-y-3">
            <div className="bg-surface-container-highest p-2 rounded flex items-center gap-2">
              <span className="material-symbols-outlined text-sm">lock</span>
              <span className="text-xs text-on-surface-variant font-mono">chrome://extensions</span>
            </div>
            <div className="text-sm text-on-surface-variant">
              Or click the puzzle icon → Manage Extensions
            </div>
          </div>
        </div>
      )
    },
    {
      number: 4,
      title: 'Enable Developer Mode',
      description: 'Toggle the "Developer mode" switch in the top-right corner of the Extensions page.',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-outline-variant/30">
          <div className="flex items-center justify-between p-4 bg-surface-container-low rounded">
            <span className="text-sm font-medium">Developer mode</span>
            <div className="w-12 h-6 bg-brand-yellow rounded-full relative">
              <div className="absolute right-1 top-1 w-4 h-4 bg-black rounded-full"></div>
            </div>
          </div>
        </div>
      )
    },
    {
      number: 5,
      title: 'Load Unpacked Extension',
      description: 'Click "Load unpacked" and select the extracted extension folder.',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-outline-variant/30">
          <div className="space-y-3">
            <button className="w-full bg-surface-container-high hover:bg-surface-container-highest text-white px-4 py-2 rounded flex items-center gap-2 justify-center transition-colors">
              <span className="material-symbols-outlined">upload_file</span>
              <span>Load unpacked</span>
            </button>
            <div className="text-xs text-on-surface-variant text-center">
              Select the folder: factcheckai-extension/extension
            </div>
          </div>
        </div>
      )
    },
    {
      number: 6,
      title: 'Pin the Extension',
      description: 'Click the puzzle icon in Chrome toolbar, find FactCheckAI, and click the pin icon.',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-outline-variant/30">
          <div className="flex items-center justify-center gap-4">
            <span className="material-symbols-outlined text-4xl text-on-surface-variant">extension</span>
            <span className="material-symbols-outlined text-2xl text-brand-yellow">push_pin</span>
          </div>
          <div className="text-xs text-on-surface-variant text-center mt-3">
            Pinned extensions appear in your toolbar
          </div>
        </div>
      )
    },
    {
      number: 7,
      title: 'Start Fact-Checking!',
      description: 'Select any text on a webpage, right-click, and choose "Check with FactCheckAI".',
      image: (
        <div className="bg-surface-container rounded-lg p-6 border border-brand-yellow/30">
          <div className="flex flex-col items-center gap-3">
            <span className="material-symbols-outlined text-6xl text-brand-yellow">check_circle</span>
            <span className="text-sm font-semibold text-white">You're all set!</span>
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 pt-24 pb-12">
        <div className="max-w-4xl mx-auto px-4 md:px-8">
          {/* Header */}
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <motion.span
              className="text-sm uppercase tracking-widest text-brand-yellow font-mono"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              Installation Guide
            </motion.span>
            <motion.h1
              className="text-4xl md:text-5xl font-bold text-white mt-3 mb-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              Install FactCheck<span className="text-brand-yellow">AI</span>
            </motion.h1>
            <motion.p
              className="text-lg text-on-surface-variant"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              Follow these simple steps to install the extension on Chrome or Edge
            </motion.p>
          </motion.div>

          {/* Steps */}
          <div className="space-y-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.number}
                className="bg-surface-container rounded-xl p-6 md:p-8 border border-outline-variant/30"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
              >
                <div className="flex items-start gap-4 mb-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-brand-yellow text-black rounded-full flex items-center justify-center font-bold text-lg">
                    {step.number}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-white mb-2">{step.title}</h3>
                    <p className="text-on-surface-variant">{step.description}</p>
                  </div>
                </div>
                
                <div className="mt-6">
                  {step.image}
                </div>

                {step.action && (
                  <div className="mt-6 flex justify-center">
                    {step.action}
                  </div>
                )}
              </motion.div>
            ))}
          </div>

          {/* Troubleshooting */}
          <motion.div
            className="mt-12 bg-surface-container-low rounded-xl p-6 border border-brand-yellow/30"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.5 }}
          >
            <div className="flex items-start gap-3">
              <span className="material-symbols-outlined text-2xl text-brand-yellow">info</span>
              <div>
                <h4 className="text-lg font-semibold text-white mb-2">Need Help?</h4>
                <p className="text-sm text-on-surface-variant mb-3">
                  If you encounter any issues during installation, please check our support page or contact us.
                </p>
                <div className="flex flex-wrap gap-3">
                  <Link
                    href="/support"
                    className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-white text-sm font-medium px-4 py-2 rounded transition-colors"
                  >
                    <span className="material-symbols-outlined text-lg">help</span>
                    <span>Support Center</span>
                  </Link>
                  <a
                    href="mailto:contact@gari.live"
                    className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-white text-sm font-medium px-4 py-2 rounded transition-colors"
                  >
                    <span className="material-symbols-outlined text-lg">email</span>
                    <span>Email Us</span>
                  </a>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Back to Home */}
          <div className="mt-8 text-center">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-brand-yellow hover:text-brand-orange transition-colors"
            >
              <span className="material-symbols-outlined">arrow_back</span>
              <span>Back to Home</span>
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
