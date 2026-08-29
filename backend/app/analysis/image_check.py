# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
Image + Text Consistency Checker

Analyzes images sent with claims using Gemini Vision.
Accepts base64 data URIs (from extension file upload) and http URLs.

Returns a description of the image and whether it's consistent with the claim.
"""
import os
import re
import base64
import logging
import requests

logger = logging.getLogger(__name__)

def _get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

GEMINI_VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_VISION_FALLBACK_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent"

# Simple rate limiter — track last vision call time to avoid 429
import threading
_last_vision_call = 0.0
_vision_lock = threading.Lock()

def _wait_for_rate_limit():
    """Ensure at least 4 seconds between vision API calls (free tier: 15 RPM)."""
    import time
    global _last_vision_call
    with _vision_lock:
        now = time.time()
        elapsed = now - _last_vision_call
        if elapsed < 4.0:
            time.sleep(4.0 - elapsed)
        _last_vision_call = time.time()

_session = requests.Session()
_session.headers.update({"User-Agent": "FactCheckerAI/2.0"})

_DATA_URI_RE = re.compile(r'^data:(image/[^;]+);base64,(.+)$', re.DOTALL)
_IMG_URL_RE  = re.compile(
    r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s"\'<>]*)?',
    re.IGNORECASE,
)


def _gemini_vision_base64(mime_type: str, b64_data: str, prompt: str) -> dict:
    """Call Gemini Vision with inline base64 image data, with retry on 429."""
    GEMINI_KEY = _get_gemini_key()
    if not GEMINI_KEY:
        return {"available": False, "reason": "No Gemini API key"}

    import time
    _wait_for_rate_limit()
    url = GEMINI_VISION_URL
    for attempt in range(3):
        try:
            r = _session.post(
                f"{url}?key={GEMINI_KEY}",
                json={
                    "contents": [{
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": b64_data}},
                        ]
                    }],
                    "generationConfig": {"temperature": 0, "maxOutputTokens": 300},
                },
                timeout=20,
            )
            if r.status_code == 429:
                wait = 2 ** attempt
                logger.warning("Gemini Vision 429 rate limit, retrying in %ss (attempt %d/3)", wait, attempt + 1)
                time.sleep(wait)
                if attempt >= 1:
                    url = GEMINI_VISION_FALLBACK_URL
                continue
            if r.status_code != 200:
                logger.warning("Gemini Vision returned %s: %s", r.status_code, r.text[:300])
                return {"available": False, "reason": f"HTTP {r.status_code}: {r.text[:100]}"}

            text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            logger.info("Gemini Vision success, description length=%d", len(text))
            return {"available": True, "description": text}
        except Exception as e:
            logger.warning("Gemini Vision failed (attempt %d): %s", attempt + 1, e)
            if attempt < 2:
                time.sleep(2 ** attempt)

    return {"available": False, "reason": "Gemini Vision rate limited after 3 attempts"}


def _gemini_vision_url(image_url: str, prompt: str) -> dict:
    """Call Gemini Vision with a public image URL."""
    GEMINI_KEY = _get_gemini_key()
    if not GEMINI_KEY:
        return {"available": False, "reason": "No Gemini API key"}
    try:
        r = _session.post(
            f"{GEMINI_VISION_URL}?key={GEMINI_KEY}",
            json={
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {"file_data": {"mime_type": "image/jpeg", "file_uri": image_url}},
                    ]
                }],
                "generationConfig": {"temperature": 0, "maxOutputTokens": 300},
            },
            timeout=15,
        )
        if r.status_code != 200:
            logger.warning("Gemini Vision URL returned %s: %s", r.status_code, r.text[:300])
            return {"available": False, "reason": f"HTTP {r.status_code}"}
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return {"available": True, "description": text}
    except Exception as e:
        logger.warning("Gemini Vision URL failed: %s", e)
        return {"available": False, "reason": str(e)}


def check_image_consistency(claim_text: str, image_source: str = "") -> dict:
    """
    Analyze an image for consistency with a claim.

    image_source can be:
    - A base64 data URI: data:image/jpeg;base64,...
    - An http/https image URL
    - Plain text (no image analysis performed)

    Returns:
        {
          "images_found": int,
          "description": str,
          "consistency": "support"|"contradict"|"neutral",
          "mismatch_risk": float 0-1,
          "flag": str | None
        }
    """
    image_source = image_source or ""
    logger.info("check_image_consistency: source_len=%d, starts_with=%s",
                len(image_source), image_source[:30] if image_source else "EMPTY")

    # Check for base64 data URI
    data_match = _DATA_URI_RE.match(image_source)
    if data_match:
        mime_type = data_match.group(1)
        b64_data  = data_match.group(2)

        prompt = (
            f"Describe what you see in this image in 2-3 sentences. "
            f"Then assess: does the image support, contradict, or is it unrelated to this claim?\n\n"
            f"Claim: {claim_text[:300]}\n\n"
            f"Format your response as:\n"
            f"Description: [what you see]\n"
            f"Assessment: support | contradict | unrelated\n"
            f"Reason: [one sentence]"
        )

        result = _gemini_vision_base64(mime_type, b64_data, prompt)
        if result.get("available"):
            desc = result["description"]
            consistency = "neutral"
            if "contradict" in desc.lower():
                consistency = "contradict"
            elif "support" in desc.lower():
                consistency = "support"

            mismatch_risk = 0.7 if consistency == "contradict" else 0.0
            return {
                "images_found":  1,
                "description":   desc,
                "consistency":   consistency,
                "mismatch_risk": mismatch_risk,
                "flag":          "image_mismatch" if mismatch_risk > 0.5 else None,
            }
        else:
            logger.warning("Gemini Vision unavailable: %s", result.get("reason"))
            return {
                "images_found":  1,
                "description":   "Image received but vision analysis unavailable",
                "consistency":   "neutral",
                "mismatch_risk": 0.0,
                "flag":          None,
            }

    # Check for http URL
    url_match = _IMG_URL_RE.search(image_source)
    if url_match:
        url    = url_match.group(0)
        prompt = f"Describe this image briefly. Does it support or contradict: {claim_text[:200]}"
        result = _gemini_vision_url(url, prompt)
        if result.get("available"):
            return {
                "images_found":  1,
                "description":   result["description"],
                "consistency":   "neutral",
                "mismatch_risk": 0.0,
                "flag":          None,
            }

    return {"images_found": 0, "checks": [], "mismatch_risk": 0.0, "flag": None}


# ── Cloud model integration (items 102, 104, 105) ────────────

def analyze_image_full(claim_text: str, image_source: str) -> dict:
    """
    Full image analysis pipeline using cloud models:
      1. Gemini Vision — description + consistency (existing)
      2. CLIP — image-text similarity score (item 104)
      3. OCR — extract text from image (item 105)
      4. Deepfake detection (item 102)

    Returns enriched result with all signals.
    """
    # Step 1: Base Gemini Vision analysis
    base = check_image_consistency(claim_text, image_source)

    # Extract image bytes for cloud models
    image_b64 = None
    if image_source and "base64," in image_source:
        image_b64 = image_source.split("base64,")[1]

    if not image_b64:
        return base

    try:
        from app.analysis.cloud_models import (
            clip_image_text_match, ocr_from_base64, detect_deepfake_b64
        )

        # Step 2: CLIP similarity (item 104)
        clip_score = clip_image_text_match(image_b64, claim_text)
        if clip_score is not None:
            base["clip_similarity"] = round(clip_score, 4)
            # Low CLIP score = image doesn't match claim
            if clip_score < 0.25:
                base["mismatch_risk"] = max(base.get("mismatch_risk", 0.0), 0.6)
                base["flag"] = "image_claim_mismatch"

        # Step 3: OCR — extract text from image (item 105)
        ocr_text = ocr_from_base64(image_b64)
        if ocr_text and len(ocr_text.strip()) > 5:
            base["ocr_text"] = ocr_text.strip()[:500]
            logger.info("OCR extracted %d chars from image", len(ocr_text))

        # Step 4: Deepfake detection (item 102)
        deepfake = detect_deepfake_b64(image_b64)
        if deepfake:
            base["deepfake"] = deepfake
            if deepfake["is_deepfake"] and deepfake["confidence"] > 0.7:
                base["mismatch_risk"] = max(base.get("mismatch_risk", 0.0), 0.85)
                base["flag"] = "deepfake_detected"
                logger.warning("Deepfake detected: confidence=%.2f", deepfake["confidence"])

    except Exception as e:
        logger.debug("Cloud image analysis failed: %s", e)

    return base


# ── SerpAPI Reverse Image Search (item 101) ──────────────────

def reverse_image_search(image_url: str) -> dict:
    """
    Reverse image search via SerpAPI to find original source of an image.
    Item 101: Detect out-of-context image reuse (old photo presented as new).

    Requires SERPAPI_KEY in environment.

    Returns:
        {
          "source_pages": list of {title, link, thumbnail},
          "earliest_date": str | None,
          "reuse_risk": float 0-1,
          "flag": str | None
        }
    """
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        logger.debug("SERPAPI_KEY not set — reverse image search skipped")
        return {"source_pages": [], "reuse_risk": 0.0, "flag": None}

    if not image_url or not image_url.startswith("http"):
        return {"source_pages": [], "reuse_risk": 0.0, "flag": None}

    try:
        r = _session.get(
            "https://serpapi.com/search",
            params={
                "engine":    "google_reverse_image",
                "image_url": image_url,
                "api_key":   serpapi_key,
                "num":       5,
            },
            timeout=15,
        )
        if r.status_code != 200:
            logger.warning("SerpAPI reverse image returned %s", r.status_code)
            return {"source_pages": [], "reuse_risk": 0.0, "flag": None}

        data = r.json()
        pages = []

        # Extract inline images / pages that show this image
        for item in data.get("inline_images", [])[:5]:
            pages.append({
                "title": item.get("title", ""),
                "link":  item.get("link", ""),
                "source": item.get("source", ""),
            })

        for item in data.get("image_results", [])[:5]:
            pages.append({
                "title": item.get("title", ""),
                "link":  item.get("link", ""),
                "source": item.get("displayed_link", ""),
            })

        # High reuse count → image may be taken out of context
        reuse_risk = min(len(pages) / 10.0, 0.7) if len(pages) > 3 else 0.0

        logger.info("Reverse image search found %d source pages, reuse_risk=%.2f",
                    len(pages), reuse_risk)

        return {
            "source_pages": pages[:5],
            "reuse_risk":   round(reuse_risk, 3),
            "flag":         "recycled_image" if reuse_risk > 0.4 else None,
        }

    except Exception as e:
        logger.debug("SerpAPI reverse image search failed: %s", e)
        return {"source_pages": [], "reuse_risk": 0.0, "flag": None}


# ── AI-Generated Image Detection (item 106) ──────────────────

_AI_IMAGE_MODEL = "umm-maybe/AI-image-detector"

def detect_ai_generated_image(image_b64: str) -> dict:
    """
    Detect whether an image was AI-generated (synthetic media).
    Item 106: Distinct from deepfake detection — catches GAN/diffusion outputs.

    Uses umm-maybe/AI-image-detector via HuggingFace Inference API.

    Returns:
        {"is_ai_generated": bool, "confidence": float, "label": str} or None
    """
    hf_token = os.getenv("HF_TOKEN", "")
    if not hf_token:
        logger.debug("HF_TOKEN not set — AI-image detection skipped")
        return None

    if "base64," in image_b64:
        image_b64 = image_b64.split("base64,")[1]

    try:
        image_bytes = base64.b64decode(image_b64)
        url = f"https://api-inference.huggingface.co/models/{_AI_IMAGE_MODEL}"
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type":  "application/octet-stream",
        }
        r = _session.post(url, headers=headers, data=image_bytes, timeout=30)

        if r.status_code == 503:
            import time; time.sleep(10)
            r = _session.post(url, headers=headers, data=image_bytes, timeout=30)

        if r.status_code != 200:
            logger.debug("AI-image detector returned %s", r.status_code)
            return None

        result = r.json()
        if not isinstance(result, list):
            return None

        # Model returns [{"label": "artificial", "score": float}, {"label": "human", "score": ...}]
        ai_score = 0.0
        human_score = 0.0
        for item in result:
            label = item.get("label", "").lower()
            score = item.get("score", 0.0)
            if "artificial" in label or "fake" in label or "generated" in label or "ai" in label:
                ai_score = score
            elif "human" in label or "real" in label or "authentic" in label:
                human_score = score

        is_ai = ai_score > 0.5
        confidence = ai_score if is_ai else human_score

        logger.info("AI-image detection: is_ai=%s confidence=%.2f", is_ai, confidence)

        return {
            "is_ai_generated": is_ai,
            "confidence":      round(confidence, 4),
            "ai_score":        round(ai_score, 4),
            "human_score":     round(human_score, 4),
            "label":           "AI_GENERATED" if is_ai else "AUTHENTIC",
            "model":           _AI_IMAGE_MODEL,
        }

    except Exception as e:
        logger.debug("AI-image detection failed: %s", e)
        return None


def analyze_image_full_extended(claim_text: str, image_source: str) -> dict:
    """
    Extended full pipeline adding SerpAPI reverse search + AI-image detection.
    Items 101, 106 completing the multimodal analysis suite.

    Extends analyze_image_full() with:
      5. SerpAPI reverse image search (item 101)
      6. AI-generated image detection (item 106)
    """
    # Run base full pipeline first (Gemini + CLIP + OCR + deepfake)
    result = analyze_image_full(claim_text, image_source)

    image_b64 = None
    image_url = None

    if image_source and "base64," in image_source:
        image_b64 = image_source.split("base64,")[1]
    else:
        url_match = _IMG_URL_RE.search(image_source or "")
        if url_match:
            image_url = url_match.group(0)

    # Step 5: Reverse image search (item 101)
    if image_url:
        reverse = reverse_image_search(image_url)
        result["reverse_image_search"] = reverse
        if reverse.get("flag"):
            result["mismatch_risk"] = max(result.get("mismatch_risk", 0.0),
                                          reverse["reuse_risk"])
            result["flag"] = result.get("flag") or reverse["flag"]

    # Step 6: AI-generated image detection (item 106)
    if image_b64:
        ai_detection = detect_ai_generated_image(image_b64)
        if ai_detection:
            result["ai_generated"] = ai_detection
            if ai_detection["is_ai_generated"] and ai_detection["confidence"] > 0.75:
                result["mismatch_risk"] = max(result.get("mismatch_risk", 0.0), 0.8)
                result["flag"] = result.get("flag") or "ai_generated_image"
                logger.warning("AI-generated image detected: confidence=%.2f",
                               ai_detection["confidence"])

    return result
