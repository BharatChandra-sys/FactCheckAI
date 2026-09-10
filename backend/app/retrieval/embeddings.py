"""
Embedding Service

Generates 384-dim sentence embeddings using all-MiniLM-L6-v2.
Falls back to a deterministic TF-IDF-based mock when sentence-transformers
is not installed (Render free tier).

All embeddings are cached in Redis (TTL: 7 days) — embeddings are stable
as long as the model doesn't change.

Usage:
    from app.retrieval.embeddings import embed, embed_batch
    vec = embed("5G towers spread COVID")   # list[float] len=384
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

EMBEDDING_DIM   = 384
_MODEL_NAME     = "all-MiniLM-L6-v2"
_CACHE_TTL      = 7 * 24 * 3600   # 7 days — embeddings are stable
_model          = None             # sentence-transformers model (lazy)
_tfidf_fallback = None             # TF-IDF vectorizer fallback


# ── Model loading ─────────────────────────────────────────────

def _load_sentence_transformer():
    global _model
    if _model is not None:
        return _model
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_MODEL_NAME)
        logger.info("Embedding model loaded: %s", _MODEL_NAME)
    except ImportError:
        logger.warning("sentence-transformers not installed — using TF-IDF fallback embeddings")
    except Exception as e:
        logger.warning("Failed to load embedding model: %s", e)
    return _model


def _tfidf_embed(text: str) -> list[float]:
    """
    Deterministic pseudo-embedding using TF-IDF hashing.
    Produces a 384-dim vector that preserves rough lexical similarity.
    NOT suitable for semantic search — only used when sentence-transformers
    is unavailable.
    """
    global _tfidf_fallback
    if _tfidf_fallback is None:
        from sklearn.feature_extraction.text import HashingVectorizer
        _tfidf_fallback = HashingVectorizer(
            n_features=EMBEDDING_DIM,
            norm="l2",
            alternate_sign=False,
        )

    vec = _tfidf_fallback.transform([text]).toarray()[0]
    return vec.tolist()


# ── Cache helpers ─────────────────────────────────────────────

def _cache_key(text: str) -> str:
    h = hashlib.sha256(text.strip().lower().encode()).hexdigest()[:16]
    return f"emb:{_MODEL_NAME}:{h}"


def _cache_get(text: str) -> Optional[list[float]]:
    try:
        from app.cache import cache
        raw = cache.get(_cache_key(text))
        if raw is not None:
            return raw if isinstance(raw, list) else json.loads(raw)
    except Exception:
        pass
    return None


def _cache_set(text: str, vec: list[float]) -> None:
    try:
        from app.cache import cache
        cache.set(_cache_key(text), vec, ttl=_CACHE_TTL)
    except Exception:
        pass


# ── Public API ────────────────────────────────────────────────

def embed(text: str) -> list[float]:
    """
    Embed a single text string.

    Returns a 384-dim float list. Uses Redis cache to avoid
    recomputing embeddings for the same text.

    Falls back to TF-IDF hashing if sentence-transformers unavailable.
    """
    text = text.strip()[:512]  # truncate to model max length

    # Cache hit
    cached = _cache_get(text)
    if cached is not None:
        return cached

    model = _load_sentence_transformer()
    if model is not None:
        try:
            vec = model.encode(text, convert_to_numpy=True).tolist()
            _cache_set(text, vec)
            return vec
        except Exception as e:
            logger.warning("Embedding failed, using fallback: %s", e)

    # Fallback
    vec = _tfidf_embed(text)
    _cache_set(text, vec)
    return vec


def embed_batch(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """
    Embed a batch of texts efficiently.

    Checks cache for each text first; only encodes uncached texts.
    Returns embeddings in the same order as the input list.
    """
    results: list[Optional[list[float]]] = [None] * len(texts)
    uncached_indices: list[int] = []
    uncached_texts:   list[str] = []

    for i, text in enumerate(texts):
        text = text.strip()[:512]
        cached = _cache_get(text)
        if cached is not None:
            results[i] = cached
        else:
            uncached_indices.append(i)
            uncached_texts.append(text)

    if uncached_texts:
        model = _load_sentence_transformer()
        if model is not None:
            try:
                vecs = model.encode(
                    uncached_texts,
                    batch_size=batch_size,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
                for idx, vec in zip(uncached_indices, vecs):
                    v = vec.tolist()
                    results[idx] = v
                    _cache_set(texts[idx], v)
            except Exception as e:
                logger.warning("Batch embedding failed: %s", e)
                # Fill with fallback
                for idx in uncached_indices:
                    if results[idx] is None:
                        results[idx] = _tfidf_embed(texts[idx])
        else:
            for idx in uncached_indices:
                results[idx] = _tfidf_embed(texts[idx])

    return [r if r is not None else [0.0] * EMBEDDING_DIM for r in results]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    va = np.array(a)
    vb = np.array(b)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)
