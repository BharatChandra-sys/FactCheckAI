'use client';

import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';

interface GitHubStats {
  stars: number;
  forks: number;
  watchers: number;
}

export default function StatsSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  const [stats, setStats] = useState<GitHubStats>({ stars: 0, forks: 0, watchers: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGitHubStats() {
      try {
        const response = await fetch('https://api.github.com/repos/BharatChandra-sys/FactCheckAI');
        if (response.ok) {
          const data = await response.json();
          setStats({
            stars: data.stargazers_count || 0,
            forks: data.forks_count || 0,
            watchers: data.subscribers_count || 0,
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

  const statCards = [
    {
      icon: 'star',
      label: 'GitHub Stars',
      value: stats.stars,
      color: 'text-brand-yellow',
      delay: 0.2
    },
    {
      icon: 'fork_right',
      label: 'Forks',
      value: stats.forks,
      color: 'text-brand-orange',
      delay: 0.3
    },
    {
      icon: 'visibility',
      label: 'Watchers',
      value: stats.watchers,
      color: 'text-secondary',
      delay: 0.4
    }
  ];

  return (
    <section className="py-12" ref={ref}>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={index}
            className="bg-surface-container rounded-xl p-6 flex flex-col items-center gap-3 border border-outline-variant/30"
            initial={{ opacity: 0, y: 30 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
            transition={{ duration: 0.6, delay: stat.delay }}
            whileHover={{ scale: 1.05, borderColor: 'rgba(251, 191, 36, 0.5)' }}
          >
            <motion.span
              className={`material-symbols-outlined text-4xl ${stat.color}`}
              initial={{ scale: 0, rotate: -180 }}
              animate={isInView ? { scale: 1, rotate: 0 } : { scale: 0, rotate: -180 }}
              transition={{ duration: 0.5, delay: stat.delay + 0.2, type: "spring" }}
            >
              {stat.icon}
            </motion.span>
            <motion.div
              className="text-4xl font-bold text-white font-mono"
              initial={{ opacity: 0 }}
              animate={isInView ? { opacity: 1 } : { opacity: 0 }}
              transition={{ duration: 0.5, delay: stat.delay + 0.4 }}
            >
              {loading ? (
                <span className="animate-pulse">...</span>
              ) : (
                <CountUp end={stat.value} duration={2} />
              )}
            </motion.div>
            <span className="text-sm text-on-surface-variant font-medium">{stat.label}</span>
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
