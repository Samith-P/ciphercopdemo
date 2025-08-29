from __future__ import annotations
import os
import time
import hashlib
import json
from pathlib import Path
from typing import Optional, Tuple
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from config_loader import AppConfig
from utils.net import guard_url, UrlError
from utils.screenshot import take_screenshot
from utils.text import extract_text_snippet
from detectors.heuristics import url_risk, brand_mismatch_score
from detectors.vision_signals import analyze_image
from detectors.gemini_mm import judge_with_image

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

app = Flask(__name__)
CFG = AppConfig(ROOT)

OUT_DIR = ROOT / "_artifacts"
OUT_DIR.mkdir(exist_ok=True)

# -------------------------
# Simple TTL In-Memory Cache
# -------------------------
CACHE: dict[str, Tuple[dict, float]] = {}
CACHE_TTL_SECONDS = 10 * 60  # 10 minutes

def get_cache(key: str) -> Optional[dict]:
    entry = CACHE.get(key)
    if not entry:
        return None
    value, ts = entry
    if time.time() - ts > CACHE_TTL_SECONDS:
        del CACHE[key]
        return None
    return value

def set_cache(key: str, value: dict):
    CACHE[key] = (value, time.time())

def make_cache_key(url: str, image_bytes: Optional[bytes]) -> str:
    h = hashlib.sha256()
    h.update((url or "").encode("utf-8"))
    if image_bytes:
        h.update(image_bytes[:100])
    return h.hexdigest()

# -------------------------
# Retry wrapper
# -------------------------
def with_retry(func, *args, retries=3, delay=3, **kwargs):
    last_exc = None
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exc = e
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise last_exc

# -------------------------
# Helpers for Gemini parsing & explanation cleanup
# -------------------------
def extract_json_from_text(text: str) -> Optional[dict]:
    """
    If text contains a JSON blob (maybe inside ```json ... ```), try to extract and parse it.
    Returns dict or None.
    """
    if not text:
        return None
    # remove leading/trailing whitespace
    t = text.strip()
    # find triple-backtick fenced JSON
    if "```json" in t or "```" in t:
        # try to find first '{' after any code fence
        try:
            # remove known code fences markers then parse first JSON object substring
            # crude but practical: find first '{' and last '}' and parse
            start = t.find("{")
            end = t.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = t[start:end+1]
                return json.loads(candidate)
        except Exception:
            pass
    # fallback: try to parse whole text as JSON
    try:
        return json.loads(t)
    except Exception:
        return None

def clean_explanation_text(text: str, max_chars: int = 600) -> str:
    """
    Remove code fences and trim to the nearest sentence under max_chars.
    """
    if not text:
        return ""
    t = text.replace("```json", "").replace("```", "").strip()
    if len(t) <= max_chars:
        return t
    # try to cut at last sentence-ending punctuation before the limit
    cut = t[:max_chars]
    last_dot = max(cut.rfind("."), cut.rfind("!"), cut.rfind("?"))
    if last_dot > 0:
        return cut[:last_dot+1]
    # otherwise return the truncated slice
    return cut + "..."

# -------------------------
# Routes
# -------------------------
@app.get("/")
def index():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    url = request.form.get("url") or (request.json or {}).get("url")
    image_bytes = None
    if "screenshot" in (request.files or {}):
        image_bytes = request.files["screenshot"].read()

    # cache key & quick lookup
    cache_key = make_cache_key(url or "", image_bytes or b"")
    if (cached := get_cache(cache_key)):
        # return cached as-is
        return jsonify({"cached": True, **cached})

    title = ""
    html = ""
    text_snippet = ""

    if url:
        try:
            guard_url(url)
        except UrlError as e:
            return jsonify({"error": f"URL blocked: {e}"}), 400

    if not image_bytes and url:
        shot_path = OUT_DIR / "shot.png"
        try:
            title, html = take_screenshot(url, shot_path, CFG.limits.get("nav_timeout_ms", 15000))
            image_bytes = shot_path.read_bytes()
        except Exception as e:
            return jsonify({"error": f"Failed to fetch page: {e}"}), 502

    if html:
        text_snippet = extract_text_snippet(html, limit=3000)

    # Heuristics
    heur = url_risk(url or "", page_text=text_snippet)

    # Vision
    vision = {"logos": [], "text": ""}
    if image_bytes:
        try:
            vision = analyze_image(image_bytes)
        except Exception as e:
            vision = {"error": f"vision_failed: {e}", "logos": [], "text": ""}

    # Brand detection (top logo)
    detected_brand = ""
    if vision.get("logos"):
        logos = sorted(vision["logos"], key=lambda x: x.get("score", 0), reverse=True)
        detected_brand = logos[0]["description"]

    # Gemini (with retry)
    gem = {"likelihood": 50, "suspected_brand": "", "explanation": ""}
    if image_bytes:
        try:
            raw_gem = with_retry(
                judge_with_image,
                image_bytes=image_bytes,
                url=url or "",
                page_title=title,
                text_snippet=text_snippet,
                authorized_brands=CFG.brands,
                retries=2, delay=5
            )
            # raw_gem may already be a dict; if it's a string try to parse
            if isinstance(raw_gem, dict):
                gem = raw_gem.copy()
            else:
                # try to interpret as JSON string
                try:
                    gem = json.loads(raw_gem)
                except Exception:
                    gem = {"likelihood": 50, "suspected_brand": "", "explanation": str(raw_gem)}
        except Exception as e:
            gem = {"likelihood": 50, "suspected_brand": "", "explanation": f"gemini_failed: {e}"}

    # If gem.explanation contains a JSON-like payload, extract and make canonical
    parsed = None
    if isinstance(gem.get("explanation"), str):
        parsed = extract_json_from_text(gem["explanation"])
    if parsed:
        # merge parsed values into gem
        if "likelihood" in parsed:
            try:
                gem["likelihood"] = int(parsed["likelihood"])
            except Exception:
                pass
        if "suspected_brand" in parsed:
            gem["suspected_brand"] = parsed.get("suspected_brand") or gem.get("suspected_brand", "")
        # prefer parsed explanation field if present
        if "explanation" in parsed:
            gem["explanation"] = parsed.get("explanation", gem.get("explanation", ""))

    # -------------------------
    # Brand mismatch scoring
    # -------------------------
    allowed_domains = []
    reg_domain = heur.get("registered_domain", "")
    brand_for_mismatch = ""

    # Prefer Gemini’s suspected brand if available, else fallback to vision
    if gem.get("suspected_brand"):
        brand_for_mismatch = gem["suspected_brand"]
    elif detected_brand:
        brand_for_mismatch = detected_brand  # <-- do not drop vision brand, always keep it

    # Lookup allowed domains for that brand
    if brand_for_mismatch:
        for b in CFG.brands:
            if b["name"].lower() in brand_for_mismatch.lower():
                allowed_domains = b.get("domains", [])
                break

    # Score mismatch: if domain doesn’t belong to brand → high risk
    brand_score = brand_mismatch_score(
        brand_for_mismatch or "",
        brand_for_mismatch or "",
        reg_domain,
        allowed_domains
    )

    # -------------------------
    # Dynamic weights
    # -------------------------
    w = CFG.weights.copy()
    if vision.get("logos"):
        w["vision_brand"] = w.get("vision_brand", 0) + 0.1
    if text_snippet and len(text_snippet) > 1000:
        w["gemini"] = w.get("gemini", 0) + 0.1

    total = sum(w.values()) or 1.0
    w = {k: v / total for k, v in w.items()}

    final = (
        w.get("gemini", 0) * (gem.get("likelihood", 50) or 0) +
        w.get("vision_brand", 0) * (brand_score or 0) +
        w.get("heuristics", 0) * (heur.get("risk", 0) or 0)
    )

    # Decision & advice
    th = CFG.thresholds
    if final >= th.get("clone", 60):
        decision = "clone"
        advice = "⚠️ Do NOT enter credentials or personal info."
    elif final >= th.get("suspicious", 30):
        decision = "suspicious"
        advice = "🟠 Be cautious — this site may be a clone. Double-check the domain."
    else:
        decision = "clean"
        advice = "🟢 Looks safe, but always verify before logging in."

    # Clean & trim explanation (prefer Gemini explanation)
    explanation_raw = gem.get("explanation") or ""
    explanation = clean_explanation_text(explanation_raw, max_chars=600)

    # Final response
    result = {
        "url": url,
        "decision": decision,
        "score": round(final, 1),
        "advice": advice,
        "explanation": explanation,
        "signals": {
            "heuristics": heur,
            "vision": {k: v for k, v in vision.items() if k != "error"},
            "gemini": gem,
            "brand_mismatch": {
                "brand": brand_for_mismatch,
                "allowed_domains": allowed_domains,
                "registered_domain": reg_domain,
                "score": brand_score,
            },
        },
        "breakdown": {
            "gemini": round(w.get("gemini", 0) * (gem.get("likelihood", 50) or 0), 1),
            "vision_brand": round(w.get("vision_brand", 0) * (brand_score or 0), 1),
            "heuristics": round(w.get("heuristics", 0) * (heur.get("risk", 0) or 0), 1),
        },
        "errors": {k: v for k, v in {"vision": vision.get("error")}.items() if v}
    }

    # cache & return
    set_cache(cache_key, result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
