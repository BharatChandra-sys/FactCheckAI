'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface GitHubStats {
  stars: number;
  forks: number;
  watchers: number;
  contributors: number;
}

export default function TrustStrip() {
  const [stats, setStats] = useState<GitHubStats>({ 
    stars: 0, 
    forks: 0, 
    watchers: 0,
    contributors: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGitHubStats() {
      try {
        // Fetch repo stats
        const repoResponse = await fetch('https://api.github.com/repos/BharatChandra-sys/FactCheckAI');
        if (repoResponse.ok) {
          const repoData = await repoResponse.json();
          
          // Fetch contributors count
          const contributorsResponse = await fetch('https://api.github.com/repos/BharatChandra-sys/FactCheckAI/contributors');
          const contributorsData = contributorsResponse.ok ? await contributorsResponse.json() : [];
          
          setStats({
            stars: repoData.stargazers_count || 0,
            forks: repoData.forks_count || 0,
            watchers: repoData.subscribers_count || 0,
            contributors: Array.isArray(contributorsData) ? contributorsData.length : 0,
          });
        }
      } catch (error) {
        console.error('Failed to fetch GitHub stats:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchGitHubStats();
  }, []);

  const statItems = [
    {
      icon: 'star',
      value: stats.stars,
      label: 'GitHub Stars',
      color: 'text-brand-yellow'
    },
    {
      icon: 'group',
      value: stats.contributors,
      label: 'Contributors',
      color: 'text-brand-orange'
    },
    {
      icon: 'fork_right',
      value: stats.forks,
      label: 'Forks',
      color: 'text-secondary'
    },
    {
      icon: 'visibility',
      value: stats.watchers,
      label: 'Watchers',
      color: 'text-on-surface-variant'
    }
  ];

  return (
    <section className="py-6 my-6">
      <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-6">
        {statItems.map((stat, index) => (
          <motion.div
            key={index}
            className="flex items-center gap-3"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <motion.span
              className={`material-symbols-outlined text-2xl ${stat.color}`}
              animate={loading ? {} : { rotate: [0, 10, -10, 0] }}
              transition={{ duration: 0.5, delay: index * 0.1 + 0.5 }}
            >
              {stat.icon}
            </motion.span>
            <div className="flex flex-col">
              <motion.span 
                className="text-2xl font-bold text-white font-mono"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
              >
                {loading ? (
                  <span className="animate-pulse">...</span>
                ) : (
                  <CountUp end={stat.value} duration={1.5} />
                )}
              </motion.span>
              <span className="text-xs text-on-surface-variant uppercase tracking-wider">
                {stat.label}
              </span>
            </div>
            {index < statItems.length - 1 && (
              <span className="text-outline-variant ml-4 hidden md:inline">|</span>
            )}
          </motion.div>
        ))}
      </div>
    </section>
  );
}

function CountUp({ end, duration }: { end: number; duration: number }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / (duration * 1000), 1);
      
      setCount(Math.floor(progress * end));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration]);

  return <>{count.toLocaleString()}</>;
}
