# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import os
import json
import time
import logging

from database import get_db
from app.auth import get_optional_user as get_current_user_optional
from app.models import User, UserFeedback, ClaimRecord

router = APIRouter(prefix="/stats", tags=["stats"])
logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

# Cache model version — only re-read when file changes
_mv_cache: dict = {}
_mv_mtime: float = 0.0

def _model_version() -> dict:
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

# Cache system stats for 2 minutes
_system_cache: dict = {}
_system_cache_ts: float = 0.0
_SYSTEM_TTL = 120.0


@router.get("")
@router.get("/")
@router.get("/system")
def system_stats(
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional),
):
    """Returns model version, drift stats, top credible sources, feedback count."""
    global _system_cache, _system_cache_ts

    now = time.time()
    if now - _system_cache_ts < _SYSTEM_TTL and _system_cache:
        return JSONResponse(
            content=_system_cache,
            headers={"Cache-Control": "public, max-age=120"},
        )

    from app.analysis.drift import get_stats as drift_stats
    from app.analysis.credibility import get_all_scores

    verdict_rows  = db.query(
        ClaimRecord.verdict, func.count(ClaimRecord.id)
    ).group_by(ClaimRecord.verdict).all()
    verdict_dist  = {v: c for v, c in verdict_rows}
    feedback_count = db.query(func.count(UserFeedback.id)).scalar() or 0
    top_sources   = get_all_scores()[:5]
    mv            = _model_version()

    result = {
        "model":          mv,
        "drift":          drift_stats(),
        "verdict_dist":   verdict_dist,
        "feedback_count": feedback_count,
        "top_sources":    top_sources,
    }
    _system_cache    = result
    _system_cache_ts = now

    return JSONResponse(
        content=result,
        headers={"Cache-Control": "public, max-age=120"},
    )


@router.get("/bias")
def publisher_bias():
    """Return political bias ratings for all tracked publishers."""
    from app.analysis.publisher_bias import get_all_bias_ratings
    return JSONResponse(
        content={"publishers": get_all_bias_ratings()},
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/calibration")
def calibration_data():
    """Calibration curve data from model_version.json."""
    mv = _model_version()
    return JSONResponse(
        content={
            "version":              mv.get("version", "unknown"),
            "accuracy":             mv.get("accuracy"),
            "f1_macro":             mv.get("f1_macro"),
            "brier_score":          mv.get("brier_score"),
            "calibration":          mv.get("calibration", "none"),
            "adversarial_f1":       mv.get("adversarial_f1"),
            "adversarial_accuracy": mv.get("adversarial_accuracy"),
            "robustness_score":     mv.get("robustness_score"),
            "adversarial_samples":  mv.get("adversarial_samples"),
            "note": "Run train_calibrated.py and eval_adversarial.py to update.",
        },
        headers={"Cache-Control": "public, max-age=300"},
    )
