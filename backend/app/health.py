# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
import os
import json
import time
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()
logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_REQUIRED_MODELS = ["model.joblib", "vectorizer.joblib", "meta_model.joblib"]

# Cache model version in memory — only re-read if file changes
_mv_cache: dict = {}
_mv_mtime: float = 0.0


def _get_model_version() -> dict:
    global _mv_cache, _mv_mtime
    path = os.path.join(_DATA_DIR, "model_version.json")
    try:
        mtime = os.path.getmtime(path)
        if mtime != _mv_mtime:
            with open(path) as f:
                _mv_cache = json.load(f)
            _mv_mtime = mtime
        return _mv_cache
    except Exception:
        return {"version": "unknown"}


def _check_db() -> dict:
    """Use pool status — no new connection needed."""
    try:
        from database import engine
        pool = engine.pool
        return {"status": "ok", "pool_size": pool.size(), "checked_in": pool.checkedin()}
    except Exception as e:
        logger.error("DB health check failed: %s", e)
        return {"status": "error", "detail": str(e)}


def _check_models() -> dict:
    missing = [f for f in _REQUIRED_MODELS if not os.path.exists(os.path.join(_DATA_DIR, f))]
    return {"status": "ok" if not missing else "degraded", "missing": missing}


@router.api_route("/health", methods=["GET", "HEAD"])
def health():
    mv       = _get_model_version()
    db_check = _check_db()
    ml_check = _check_models()

    overall = "ok"
    if db_check["status"] != "ok":
        overall = "degraded"
    if ml_check["status"] != "ok":
        overall = "degraded"

    payload = {
        "status":  overall,
        "version": "2.0.0",
        "ts":      int(time.time()),
        "model":   mv,
        "checks": {
            "database": db_check,
            "models":   ml_check,
        },
    }

    status_code = 200 if overall == "ok" else 503
    return JSONResponse(
        content=payload,
        status_code=status_code,
        headers={"Cache-Control": "no-cache, no-store"},
    )


@router.api_route("/health/detailed", methods=["GET"])
def health_detailed():
    """Detailed health including drift stats — not used by load balancer pings."""
    base = health()
    try:
        from app.analysis.drift import get_stats as drift_stats
        import json as _json
        payload = _json.loads(base.body)
        payload["drift"] = drift_stats()
        return JSONResponse(
            content=payload,
            status_code=base.status_code,
            headers={"Cache-Control": "no-cache, no-store"},
        )
    except Exception:
        return base
