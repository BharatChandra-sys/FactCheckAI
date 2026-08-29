# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

_db_dir = os.path.dirname(os.path.abspath(__file__))
_default_db = f"sqlite:///{os.path.join(_db_dir, 'fake_news.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", _default_db)

# Fix relative sqlite paths
if DATABASE_URL.startswith("sqlite:///./"):
    rel_path = DATABASE_URL[len("sqlite:///./"):]
    DATABASE_URL = f"sqlite:///{os.path.join(_db_dir, rel_path)}"

# Render gives postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
    # Enable WAL mode for SQLite — dramatically improves concurrent read/write
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-64000")   # 64MB page cache
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL production settings
    # pool_size tuned for Aiven free tier (~25 max connections)
    # Each gunicorn worker gets its own pool so total = workers × pool_size
    _workers = int(os.getenv("WEB_CONCURRENCY", "2"))
    _pool_per_worker = max(2, 18 // _workers)   # stay well under 25 total

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,          # reconnect on stale connections
        pool_size=_pool_per_worker,
        max_overflow=2,              # small burst headroom
        pool_timeout=20,             # fail fast — don't queue too long
        pool_recycle=900,            # recycle every 15 min (avoids idle timeout)
        # Explicit statement timeout — kills runaway queries
        connect_args={
            "options": "-c statement_timeout=30000",   # 30s max query time
            "connect_timeout": 10,
        },
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
