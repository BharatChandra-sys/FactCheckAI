# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
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

# ── Neon-specific: strip pgbouncer=true from SQLAlchemy URL ──
# pgbouncer=true is a Neon hint for their proxy — SQLAlchemy doesn't understand it.
# We use it to detect when pooled mode is active and set pool_pre_ping accordingly.
_is_neon_pooled = "pgbouncer=true" in DATABASE_URL
if _is_neon_pooled:
    DATABASE_URL = DATABASE_URL.replace("&pgbouncer=true", "").replace("?pgbouncer=true", "")
    # Rebuild query string correctly if pgbouncer was the only param
    if DATABASE_URL.endswith("?"):
        DATABASE_URL = DATABASE_URL[:-1]

if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
    # WAL mode — dramatically improves concurrent read/write
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-64000")   # 64MB page cache
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL / Neon production settings
    # Neon free tier: up to 100 pooled connections via pgBouncer
    # Render free: 1 worker — pool_size=2 is enough
    _workers = int(os.getenv("WEB_CONCURRENCY", "1"))
    _pool_per_worker = max(2, 10 // _workers)

    _connect_args = {
        "connect_timeout": 10,
    }

    # statement_timeout must NOT be sent via the pooled Neon URL (pgBouncer blocks it)
    # Only add it when using a direct (non-pooled) connection
    _is_pooled_url = "pooler" in DATABASE_URL
    if not _is_pooled_url:
        _connect_args["options"] = "-c statement_timeout=30000"

    # Neon requires sslmode=require — enforce it
    if "neon.tech" in DATABASE_URL and "sslmode" not in DATABASE_URL:
        DATABASE_URL += ("&" if "?" in DATABASE_URL else "?") + "sslmode=require"

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,          # detects stale connections (Neon auto-suspend)
        pool_size=_pool_per_worker,
        max_overflow=2,
        pool_timeout=20,
        pool_recycle=900,            # recycle every 15 min (before Neon idles)
        connect_args=_connect_args,
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
