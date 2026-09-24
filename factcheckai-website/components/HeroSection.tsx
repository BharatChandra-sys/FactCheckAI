'use client';

import { motion } from 'framer-motion';

export default function HeroSection() {
  return (
    <section className="relative py-8 md:py-12 overflow-hidden" id="product">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Column: Copy & Actions */}
        <motion.div 
          className="lg:col-span-7 flex flex-col gap-4"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          {/* Main Headline */}
          <motion.h1 
            className="text-4xl md:text-5xl font-bold text-white tracking-tight max-w-2xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Stop misinformation before it spreads. <br className="hidden sm:inline" />
            <span className="text-brand-yellow">Get the truth instantly.</span>
          </motion.h1>

          {/* Supporting Copy */}
          <motion.p 
            className="text-lg text-on-surface-variant max-w-xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            FactCheckAI analyzes claims in real-time using advanced AI models and cross-references millions of trusted sources. Know what's true while you browse.
          </motion.p>

          {/* Dual CTA */}
          <motion.div 
            className="flex flex-wrap items-center gap-4 pt-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <motion.a
              href="/install"
              className="inline-flex items-center gap-2 bg-brand-yellow hover:bg-brand-orange text-black text-base font-semibold px-6 py-2.5 rounded shadow-sm transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="material-symbols-outlined text-xl">extension</span>
              <span>Install Extension</span>
            </motion.a>

            <motion.a
              href="#how-it-works"
              onClick={(e) => {
                e.preventDefault();
                const element = document.getElementById('how-it-works');
                element?.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }}
              className="inline-flex items-center gap-2 bg-surface-container-high hover:bg-surface-container-highest text-white text-base font-medium px-4 py-2.5 rounded transition-colors shadow-sm"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="material-symbols-outlined text-xl">play_circle</span>
              <span>See How It Works</span>
            </motion.a>
          </motion.div>
        </motion.div>

        {/* Right Column: Interactive Browser Extension Card */}
        <motion.div 
          className="lg:col-span-5 flex justify-center"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <motion.div 
            className="w-full max-w-[430px] rounded-xl bg-surface-container p-4 shadow-2xl flex flex-col gap-4"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.3 }}
          >
            {/* Extension Header */}
            <div className="flex items-center justify-between pb-2">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-white">FactCheckAI</span>
                <span className="text-xs bg-surface-container-highest text-on-surface-variant px-1.5 py-0.5 rounded">
                  Extension
                </span>
              </div>
              <div className="flex items-center gap-1 bg-surface-container-lowest px-2 py-0.5 rounded text-xs text-on-surface-variant">
                <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                <span>Active DOM</span>
              </div>
            </div>

            {/* Highlight Target Origin */}
            <div className="bg-surface-container-low p-2 rounded flex items-center justify-between text-on-surface-variant text-xs">
              <span className="truncate max-w-60">en.wikipedia.org / social_thread#8402</span>
              <span className="text-outline uppercase">Selected span</span>
            </div>

            {/* The Evaluated Claim */}
            <motion.div 
              className="bg-surface-container-lowest p-3 rounded flex flex-col gap-1"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.8 }}
            >
              <span className="text-xs text-outline uppercase tracking-wider">Claim detected:</span>
              <p className="text-sm text-white font-medium italic">
                "5G towers spread coronavirus through high-frequency radio waves."
              </p>
            </motion.div>

            {/* Verdict Block: FAKE */}
            <motion.div 
              className="p-3 rounded bg-error-container/20 flex flex-col gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 1 }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-lg text-error">cancel</span>
                  <span className="text-sm font-semibold text-error uppercase tracking-wider">VERDICT: FAKE</span>
                </div>
                <span className="text-sm text-error font-mono">87.4% CONFIDENCE</span>
              </div>
              {/* Horizontal Segmented Confidence Meter */}
              <div className="w-full bg-surface-container-highest h-1.5 rounded-full overflow-hidden flex">
                <motion.div 
                  className="bg-error h-full rounded-full" 
                  initial={{ width: '0%' }}
                  animate={{ width: '87.4%' }}
                  transition={{ duration: 1, delay: 1.2, ease: "easeOut" }}
                />
              </div>
            </motion.div>

            {/* Short Scientific Explanation */}
            <motion.p 
              className="text-xs text-on-surface-variant leading-relaxed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 1.3 }}
            >
              Multiple international public health authorities and telecommunications engineering bodies confirm non-ionizing electromagnetic radiation cannot synthesize or transmit biological viral matter.
            </motion.p>

            {/* Evidence List */}
            <motion.div 
              className="flex flex-col gap-1.5"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 1.5 }}
            >
              <div className="flex items-center justify-between text-on-surface-variant text-xs pb-1">
                <span className="uppercase tracking-wider">Top Validated Sources</span>
                <span>Vector Sim: 0.94</span>
              </div>

              {/* Source 1 */}
              <motion.div 
                className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs"
                whileHover={{ x: 5 }}
                transition={{ duration: 0.2 }}
              >
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-white truncate font-medium">WHO Global Health Brief (2020)</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">98% STRENGTH</span>
              </motion.div>

              {/* Source 2 */}
              <motion.div 
                className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs"
                whileHover={{ x: 5 }}
                transition={{ duration: 0.2 }}
              >
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-white truncate font-medium">IEEE Microwave Theory Report</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">94% STRENGTH</span>
              </motion.div>

              {/* Source 3 */}
              <motion.div 
                className="flex items-center justify-between p-2 bg-surface-container-low hover:bg-surface-container-high rounded transition-colors text-xs"
                whileHover={{ x: 5 }}
                transition={{ duration: 0.2 }}
              >
                <div className="flex items-center gap-1.5 truncate">
                  <span className="material-symbols-outlined text-sm text-secondary">verified</span>
                  <span className="text-white truncate font-medium">Reuters Fact Verification Archive</span>
                </div>
                <span className="text-xs text-secondary bg-secondary/10 px-1 rounded ml-2 shrink-0">91% STRENGTH</span>
              </motion.div>
            </motion.div>

            {/* Popup Action Footer */}
            <div className="flex items-center justify-between pt-2 text-xs text-outline">
              <span className="font-mono">RoBERTa-v2 + Hybrid RAG</span>
              <div className="flex items-center gap-2">
                <motion.button 
                  className="px-2 py-1 bg-surface-container-high hover:bg-surface-container-highest text-white rounded transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Reasoning Chain
                </motion.button>
                <motion.button 
                  className="px-2 py-1 bg-brand-yellow text-black font-semibold rounded hover:bg-brand-orange transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  View All (3)
                </motion.button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
