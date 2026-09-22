'use client';

import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';

export default function BrowserExtension() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <section className="py-8 flex flex-col gap-8" ref={ref}>
      <motion.div 
        className="flex flex-col gap-2 max-w-2xl"
        initial={{ opacity: 0, y: 30 }}
        animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
        transition={{ duration: 0.6 }}
      >
        <motion.span 
          className="text-sm uppercase tracking-widest text-brand-yellow font-mono"
          initial={{ opacity: 0, x: -20 }}
          animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          05 // Browser Integration
        </motion.span>
        <motion.h2 
          className="text-4xl font-bold text-white"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          Check claims without leaving your tab
        </motion.h2>
        <motion.p 
          className="text-lg text-on-surface-variant"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          Select any text on any webpage. Right-click to invoke FactCheckAI. Get instant verdicts with sourced evidence—no tab switching required.
        </motion.p>
      </motion.div>

      {/* Browser Mockup */}
      <motion.div 
        className="bg-surface-container rounded-xl p-6 shadow-2xl"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }}
        transition={{ duration: 0.7, delay: 0.5 }}
      >
        <div className="bg-surface-container-low rounded-lg overflow-hidden">
          {/* Browser Chrome */}
          <motion.div 
            className="bg-surface-container-highest p-3 flex items-center gap-3 border-b border-outline-variant/30"
            initial={{ opacity: 0, y: -10 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: -10 }}
            transition={{ duration: 0.5, delay: 0.7 }}
          >
            <div className="flex items-center gap-1.5">
              <motion.div 
                className="w-3 h-3 rounded-full bg-error"
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : { scale: 0 }}
                transition={{ duration: 0.3, delay: 0.8 }}
              />
              <motion.div 
                className="w-3 h-3 rounded-full bg-brand-yellow"
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : { scale: 0 }}
                transition={{ duration: 0.3, delay: 0.85 }}
              />
              <motion.div 
                className="w-3 h-3 rounded-full bg-secondary"
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : { scale: 0 }}
                transition={{ duration: 0.3, delay: 0.9 }}
              />
            </div>
            <motion.div 
              className="flex-1 bg-surface-container px-4 py-1.5 rounded text-xs text-on-surface-variant font-mono"
              initial={{ opacity: 0, width: 0 }}
              animate={isInView ? { opacity: 1, width: "auto" } : { opacity: 0, width: 0 }}
              transition={{ duration: 0.5, delay: 0.95 }}
            >
              https://example-news-site.com/article/breaking-news
            </motion.div>
            <motion.span 
              className="material-symbols-outlined text-brand-yellow text-lg"
              initial={{ opacity: 0, rotate: -180 }}
              animate={isInView ? { opacity: 1, rotate: 0 } : { opacity: 0, rotate: -180 }}
              transition={{ duration: 0.5, delay: 1 }}
            >
              extension
            </motion.span>
          </motion.div>

          {/* Page Content with Highlighted Claim */}
          <div className="p-6 space-y-4">
            <motion.h3 
              className="text-xl font-bold text-white"
              initial={{ opacity: 0, x: -20 }}
              animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.5, delay: 1.1 }}
            >
              Breaking: New Study Claims...
            </motion.h3>
            <motion.p 
              className="text-base text-on-surface-variant leading-relaxed"
              initial={{ opacity: 0 }}
              animate={isInView ? { opacity: 1 } : { opacity: 0 }}
              transition={{ duration: 0.5, delay: 1.2 }}
            >
              According to researchers at the university,{' '}
              <motion.span 
                className="bg-brand-yellow/20 text-white font-medium px-1 rounded relative"
                initial={{ backgroundColor: "rgba(251, 191, 36, 0)" }}
                animate={isInView ? { backgroundColor: "rgba(251, 191, 36, 0.2)" } : { backgroundColor: "rgba(251, 191, 36, 0)" }}
                transition={{ duration: 0.5, delay: 1.4 }}
              >
                "synthetic vitamin supplements are now considered toxic by WHO"
                <motion.span 
                  className="absolute -top-1 -right-1 w-2 h-2 bg-error rounded-full"
                  initial={{ scale: 0 }}
                  animate={isInView ? { scale: [0, 1.2, 1] } : { scale: 0 }}
                  transition={{ duration: 0.5, delay: 1.6, repeat: Infinity, repeatDelay: 1 }}
                />
              </motion.span>
              , sparking controversy in the medical community.
            </motion.p>

            {/* Context Menu Popup */}
            <motion.div 
              className="ml-12 mt-4 bg-surface-container p-4 rounded-lg shadow-2xl border border-brand-yellow/30 max-w-md"
              initial={{ opacity: 0, scale: 0.9, y: -20 }}
              animate={isInView ? { opacity: 1, scale: 1, y: 0 } : { opacity: 0, scale: 0.9, y: -20 }}
              transition={{ duration: 0.5, delay: 1.7, type: "spring", stiffness: 100 }}
            >
              <div className="flex flex-col gap-3">
                <motion.div 
                  className="flex items-center gap-2 pb-2 border-b border-outline-variant/30"
                  initial={{ opacity: 0 }}
                  animate={isInView ? { opacity: 1 } : { opacity: 0 }}
                  transition={{ duration: 0.3, delay: 1.9 }}
                >
                  <span className="text-sm font-semibold text-white">FactCheckAI</span>
                </motion.div>
                <motion.div 
                  className="flex items-center gap-2 text-xs"
                  initial={{ opacity: 0, x: -10 }}
                  animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -10 }}
                  transition={{ duration: 0.3, delay: 2 }}
                >
                  <span className="material-symbols-outlined text-error text-base">cancel</span>
                  <span className="font-semibold text-error">VERDICT: FAKE (87% confidence)</span>
                </motion.div>
                <motion.p 
                  className="text-xs text-on-surface-variant leading-relaxed"
                  initial={{ opacity: 0 }}
                  animate={isInView ? { opacity: 1 } : { opacity: 0 }}
                  transition={{ duration: 0.3, delay: 2.1 }}
                >
                  No WHO declaration matches this claim. Cross-referenced with 3 official sources showing no toxicity classification exists.
                </motion.p>
                <motion.button 
                  className="bg-brand-yellow text-black text-xs font-semibold px-3 py-1.5 rounded hover:bg-brand-orange transition-colors"
                  initial={{ opacity: 0, y: 10 }}
                  animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 10 }}
                  transition={{ duration: 0.3, delay: 2.2 }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  View Full Analysis
                </motion.button>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            icon: 'bolt',
            color: 'text-brand-yellow',
            title: 'Instant Context Menu',
            description: 'Right-click any selected text to trigger instant fact-checking without opening new tabs.',
            delay: 0.2
          },
          {
            icon: 'highlight',
            color: 'text-secondary',
            title: 'Visual Highlights',
            description: 'Suspicious claims are automatically highlighted with color-coded severity indicators.',
            delay: 0.3
          },
          {
            icon: 'history',
            color: 'text-brand-orange',
            title: 'Session History',
            description: 'Review all fact-checks from your browsing session with full evidence trails.',
            delay: 0.4
          }
        ].map((feature, index) => (
          <motion.div 
            key={index}
            className="flex flex-col gap-2"
            initial={{ opacity: 0, y: 30 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.5, delay: 2.3 + feature.delay }}
            whileHover={{ scale: 1.05, y: -5 }}
          >
            <motion.span 
              className={`material-symbols-outlined text-2xl ${feature.color}`}
              initial={{ scale: 0, rotate: -180 }}
              animate={isInView ? { scale: 1, rotate: 0 } : { scale: 0, rotate: -180 }}
              transition={{ duration: 0.5, delay: 2.4 + feature.delay, type: "spring" }}
            >
              {feature.icon}
            </motion.span>
            <h4 className="text-lg font-semibold text-white">{feature.title}</h4>
            <p className="text-sm text-on-surface-variant">{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
