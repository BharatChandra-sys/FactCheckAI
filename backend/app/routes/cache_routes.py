# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
Cache Management Routes

Endpoints for cache statistics and management.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
import os

from app.cache import cache, invalidate_model_cache, invalidate_claim_cache
from app.auth import get_current_user
from app.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cache", tags=["cache"])

# Admin emails from env — comma-separated
_ADMIN_EMAILS = {e.strip().lower() for e in os.getenv("ADMIN_EMAILS", "").split(",") if e.strip()}


def _require_admin(user: User = Depends(get_current_user)) -> User:
    """Allow only admin emails to call destructive cache operations."""
    if _ADMIN_EMAILS and user.email.lower() not in _ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.get("/stats")
async def get_cache_stats(user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Get cache statistics. Requires authentication."""
    return cache.get_stats()


@router.post("/invalidate/model/{model_version}")
async def invalidate_model(
    model_version: str,
    user: User = Depends(_require_admin)
):
    """
    Invalidate all caches for a specific model version.
    
    This should be called when a new model is deployed to ensure
    predictions are recomputed with the new model.
    
    Requires authentication.
    """
    try:
        deleted = invalidate_model_cache(model_version)
        return {
            "success": True,
            "message": f"Invalidated cache for model {model_version}",
            "deleted_keys": deleted
        }
    except Exception as e:
        logger.error(f"Cache invalidation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/invalidate/claim")
async def invalidate_claim(
    claim_text: str,
    user: User = Depends(_require_admin)
):
    """
    Invalidate cache for a specific claim.
    
    This can be used when a claim's verdict needs to be recomputed
    (e.g., after new evidence becomes available).
    
    Requires authentication.
    """
    try:
        invalidate_claim_cache(claim_text)
        return {
            "success": True,
            "message": "Claim cache invalidated",
            "claim": claim_text[:100]
        }
    except Exception as e:
        logger.error(f"Claim cache invalidation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_cache(user: User = Depends(_require_admin)):
    """
    Clear all cache entries.
    
    WARNING: This will delete all cached data and may cause
    temporary performance degradation.
    
    Requires authentication.
    """
    try:
        if not cache.is_available():
            raise HTTPException(status_code=503, detail="Cache not available")
        
        # Delete all keys
        deleted = cache.delete_pattern("*")
        
        return {
            "success": True,
            "message": "Cache cleared",
            "deleted_keys": deleted
        }
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def cache_health():
    """
    Check cache health status.
    
    Returns:
    - available: Whether cache is available
    - latency_ms: Ping latency in milliseconds
    """
    import time
    
    if not cache.is_available():
        return {
            "available": False,
            "message": "Cache not enabled or not connected"
        }
    
    try:
        start = time.time()
        cache.client.ping()
        latency = (time.time() - start) * 1000
        
        return {
            "available": True,
            "latency_ms": round(latency, 2),
            "message": "Cache is healthy"
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "message": "Cache health check failed"
        }
