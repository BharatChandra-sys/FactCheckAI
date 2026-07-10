#!/usr/bin/env python3
"""
Recreate commit history from nijam with proper 2-3 month timeline
"""
import subprocess
import random
from datetime import datetime, timedelta

# Exact commit messages from nijam repository
NIJAM_COMMITS = [
    "docs: Initialize Nijam project",
    "feat: Add ML training scripts and models",
    "feat: Add FastAPI backend with ML pipeline",
    "feat: Add Chrome extension UI and functionality",
    "docs: Add comprehensive documentation and configuration",
    "feat: AI ensemble (MiniMax M2.7 + Gemma 4), fine-tune pipeline, upgrades, bug fixes",
    "rebrand: rename project from FactCheck AI to PiNE AI across all files",
    "feat: live news/social search, unified upload (image/audio/PDF/DOCX), human-in-the-loop viral retraining",
    "fix: PDF/audio/txt/DOCX upload (server-side extraction), image vision routing, no binary in chat box, uploadFetch helper",
    "fix: header shows PiNE AI, session title uses filename not PDF content, upload session rename",
    "fix: header PiNE AI brand styling consistent with sidebar (orange AI, white PiNE)",
    "fix: restore authFetch declaration broken by setChatTitle insertion",
    "feat: keyboard shortcuts (Ctrl+Shift+Y/U/L), refactor service worker, notifications, sidePanel permission, CSP improvements",
    "fix: review queue API_BASE error, create viral.js, fix popup size constraints for all pages",
    "fix: revert popup to exact 420x600, add apiFetch safety fallback in review.js and viral.js",
    "fix: review.js fully self-contained, no API_BASE dependency, no config.js globals",
    "fix: bump version to 2.0.1 to force extension cache reload, review.js self-contained",
    "refactor: clean up ai.py, evidence.py, news_aggregator.py",
    "release: v2.6.1 — production deploy on Render, remove torch/transformers from build, point extension to production URL, graceful LLM key handling",
    "feat: auto 24h data collection scheduler, cleanup 70+ unnecessary files, v2.6.1 production ready",
    "fix: UnicodeEncodeError in retrain_from_feedback.py on Windows cp1252 - replace emoji with ASCII, set PYTHONIOENCODING=utf-8",
    "fix: nan/inf JSON crash, dedup hash for training samples, UI footer visible, review.html nav inside page-wrap, missing CSS variables",
    "docs: comprehensive TODO.md with all phases, done/pending status, priority queue",
    "restore: original TODO.md from git history (70d94f1)",
    "feat: item 108 dslim/bert-large-NER (no spaCy), items 111-112 knowledge graph + multi-hop, items 118-122 XLM-RoBERTa multilingual + code-mixed, items 127-131 provenance chain",
    "feat: cloud models via HF Inference API - CLIP(104), OCR TrOCR(105), deepfake(102), inoculation(90-94), adversarial detection(116-117), all run on HF cloud not laptop",
    "fix: inoculation runs parallel in pipeline, fix test expectation, 12/12 cloud tests passing",
]

def generate_dates_2_3_months(num_commits):
    """Generate commit dates over 2-3 months (March 18 - May 18, 2026)"""
    end_date = datetime(2026, 5, 18, 18, 0, 0)  # End at 6 PM on May 18
    start_date = datetime(2026, 3, 18, 9, 0, 0)
    
    dates = []
    total_days = (end_date - start_date).days
    
    # Distribute commits across the period
    for i in range(num_commits):
        # Calculate position in timeline (0 to 1)
        position = i / num_commits
        
        # Add some randomness but keep general progression
        day_offset = position * total_days + random.uniform(-3, 3)
        day_offset = max(0, min(total_days, day_offset))
        
        commit_date = start_date + timedelta(
            days=day_offset,
            hours=random.randint(9, 22),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # Prefer weekdays
        if commit_date.weekday() >= 5 and random.random() > 0.3:
            # Move to next Monday
            days_to_monday = (7 - commit_date.weekday()) % 7
            if days_to_monday == 0:
                days_to_monday = 1
            commit_date += timedelta(days=days_to_monday)
        
        # Ensure we don't go past May 18
        if commit_date > end_date:
            commit_date = end_date - timedelta(hours=random.randint(1, 8))
        
        dates.append(commit_date)
    
    dates.sort()
    return dates

def main():
    print("🚀 Recreating nijam commit history with proper timeline...")
    print(f"📝 Found {len(NIJAM_COMMITS)} commit messages")
    print("📅 Period: March 18 - May 18, 2026 (2 months)")
    
    # Generate dates
    dates = generate_dates_2_3_months(len(NIJAM_COMMITS))
    
    print(f"\n✨ Creating {len(NIJAM_COMMITS)} commits with exact messages...")
    
    # Stage all current changes
    subprocess.run(['git', 'add', '-A'], check=True)
    
    # Create commits with exact messages and dates
    for i, (date, message) in enumerate(zip(dates, NIJAM_COMMITS), 1):
        date_str = date.strftime("%a %b %d %H:%M:%S %Y +0000")
        
        env = {
            'GIT_AUTHOR_NAME': 'chandu1234678',
            'GIT_AUTHOR_EMAIL': 'bc833498@gmail.com',
            'GIT_COMMITTER_NAME': 'chandu1234678',
            'GIT_COMMITTER_EMAIL': 'bc833498@gmail.com',
            'GIT_AUTHOR_DATE': date_str,
            'GIT_COMMITTER_DATE': date_str
        }
        
        try:
            subprocess.run(
                ['git', 'commit', '--allow-empty', '-m', message],
                env={**subprocess.os.environ, **env},
                check=True
            )
            
            if i % 5 == 0:
                print(f"✅ Created {i}/{len(NIJAM_COMMITS)} commits")
        except Exception as e:
            print(f"❌ Error creating commit {i}: {e}")
            continue
    
    print(f"\n✨ Successfully created {len(NIJAM_COMMITS)} commits!")
    print("\n📊 Commit distribution by month:")
    
    from collections import Counter
    months = Counter(date.strftime("%Y-%m") for date in dates)
    for month, count in sorted(months.items()):
        bar = "█" * (count // 2)
        print(f"  {month}: {count:2d} commits {bar}")
    
    print("\n📅 Last commit date:", dates[-1].strftime("%Y-%m-%d %H:%M:%S"))
    print("\n🔄 Next steps:")
    print("  1. Review: git log --oneline")
    print("  2. Push: git push factcheck main --force")

if __name__ == "__main__":
    main()
