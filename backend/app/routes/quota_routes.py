# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
Quota Management Routes

Endpoints for checking and managing user quotas and rate limits.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
from datetime import datetime, timedelta

from database import get_db
from app.models import User, ClaimRecord
from app.auth import get_current_user
from app.rate_limit import rate_limiter, TIER_LIMITS
from sqlalchemy import func

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quota", tags=["quota"])


@router.get("/usage")
async def get_usage(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current user's usage statistics and quota information.
    
    Returns:
    - tier: User's subscription tier
    - limits: Rate limits for this tier
    - usage: Current month's usage
    - quota: Monthly quota information
    """
    tier = rate_limiter.get_user_tier(user)
    tier_config = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    
    # Get current month's usage
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    
    # Count claims this month via ClaimRecord.user_id (added in enterprise migration)
    claims_this_month = db.query(func.count(ClaimRecord.id)).filter(
        ClaimRecord.user_id == user.id,
        ClaimRecord.created_at >= month_start,
        ClaimRecord.created_at <= month_end,
    ).scalar() or 0

    total_claims = db.query(func.count(ClaimRecord.id)).filter(
        ClaimRecord.user_id == user.id,
    ).scalar() or 0
    
    # Calculate quota info
    monthly_limit = tier_config.get("monthly_claims", 100)
    quota_remaining = max(0, monthly_limit - claims_this_month) if monthly_limit != -1 else -1
    
    # Calculate reset time
    next_month = (month_start + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return {
        "tier": tier,
        "limits": {
            "per_minute": tier_config.get("per_minute"),
            "per_hour": tier_config.get("per_hour"),
            "per_day": tier_config.get("per_day"),
            "monthly_claims": tier_config.get("monthly_claims"),
        },
        "usage": {
            "claims_this_month": claims_this_month,
            "total_claims": total_claims,
        },
        "quota": {
            "limit": monthly_limit,
            "used": claims_this_month,
            "remaining": quota_remaining,
            "reset_at": int(next_month.timestamp()),
            "reset_date": next_month.isoformat(),
        }
    }


@router.get("/tiers")
async def get_tiers() -> Dict[str, Any]:
    """
    Get information about all available subscription tiers.
    
    Returns tier limits and pricing information.
    """
    return {
        "tiers": {
            "free": {
                "name": "Free",
                "price": 0,
                "limits": TIER_LIMITS["free"],
                "features": [
                    "30 requests per day",
                    "Basic fact-checking",
                    "Evidence from trusted sources",
                    "ML + AI analysis",
                    "Community support",
                ]
            },
            "pro": {
                "name": "Pro",
                "price": 9.99,
                "limits": TIER_LIMITS["pro"],
                "features": [
                    "1,000 claims per month",
                    "Priority processing",
                    "Advanced analytics",
                    "SHAP explanations",
                    "Email support",
                ]
            },
            "enterprise": {
                "name": "Enterprise",
                "price": 99.99,
                "limits": TIER_LIMITS["enterprise"],
                "features": [
                    "Unlimited claims",
                    "Dedicated support",
                    "Custom integrations",
                    "API access",
                    "SLA guarantee",
                ]
            }
        }
    }


@router.post("/upgrade")
async def upgrade_tier(
    target_tier: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Tier upgrade endpoint — disabled until payment integration is complete.
    Returns 501 Not Implemented to prevent free tier escalation.
    """
    raise HTTPException(
        status_code=501,
        detail="Tier upgrades are not yet available. Contact support to upgrade your account."
    )


@router.get("/history")
async def get_usage_history(
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get usage history for the past N days.
    
    Returns daily claim counts for visualization.
    """
    from sqlalchemy import func, cast, Date

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    results = db.query(
        cast(ClaimRecord.created_at, Date).label("date"),
        func.count(ClaimRecord.id).label("count")
    ).filter(
        ClaimRecord.user_id == user.id,
        ClaimRecord.created_at >= cutoff_date,
    ).group_by(
        cast(ClaimRecord.created_at, Date)
    ).order_by(
        cast(ClaimRecord.created_at, Date)
    ).all()
    
    # Format results
    history = [
        {
            "date": str(row.date),
            "claims": row.count
        }
        for row in results
    ]
    
    return {
        "days": days,
        "history": history,
        "total": sum(row["claims"] for row in history)
    }


@router.get("/rate-limit-status")
async def get_rate_limit_status(
    user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current rate limit status for all windows.
    
    Returns remaining requests for minute, hour, and day windows.
    """
    tier = rate_limiter.get_user_tier(user)
    identifier = f"user:{user.id}"
    
    status = {}
    for window in ["minute", "hour", "day"]:
        allowed, info = rate_limiter.check_rate_limit(
            identifier, tier, "/message", window
        )
        status[window] = {
            "limit": info.get("limit", 0),
            "remaining": info.get("remaining", 0),
            "reset": info.get("reset", 0),
        }
    
    return {
        "tier": tier,
        "status": status
    }
