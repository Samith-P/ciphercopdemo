from __future__ import annotations
import os, io, json
from pathlib import Path
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config_loader import AppConfig
from utils.net import guard_url, UrlError
from utils.screenshot import take_screenshot
from utils.text import extract_text_snippet
from detectors.heuristics import url_risk, brand_mismatch_score
from detectors.vision_signals import analyze_image
from detectors.gemini_mm import judge_with_image
from flask import render_template


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

app = Flask(__name__)
CFG = AppConfig(ROOT)

OUT_DIR = ROOT / "_artifacts"; OUT_DIR.mkdir(exist_ok=True)

@app.get("/")
def index():
    return render_template("index.html")

    
    
@app.post("/analyze")
def analyze():
    url = request.form.get("url") or (request.json or {}).get("url")
    image_bytes = None
    if "screenshot" in (request.files or {}):
        image_bytes = request.files["screenshot"].read()

    title = ""; html = ""; text_snippet = ""

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

    # Brand detection
    detected_brand = ""
    if vision.get("logos"):
        logos = sorted(vision["logos"], key=lambda x: x.get("score", 0), reverse=True)
        detected_brand = logos[0]["description"]

    # Gemini
    gem = {"likelihood": 50, "suspected_brand": "", "explanation": ""}
    if image_bytes:
        try:
            gem = judge_with_image(
                image_bytes=image_bytes,
                url=url or "",
                page_title=title,
                text_snippet=text_snippet,
                authorized_brands=CFG.brands,
            )
        except Exception as e:
            gem = {"likelihood": 50, "suspected_brand": "", "explanation": f"gemini_failed: {e}"}

    # Brand mismatch score
    allowed_domains = []
    brand_for_mismatch = gem.get("suspected_brand") or detected_brand
    reg_domain = heur.get("registered_domain", "")

    if brand_for_mismatch:
        for b in CFG.brands:
            if b["name"].lower() in brand_for_mismatch.lower():
                allowed_domains = b.get("domains", [])
                break

    brand_score = brand_mismatch_score(
        brand_for_mismatch or "", brand_for_mismatch or "", reg_domain, allowed_domains
    )

    # Final score
    w = CFG.weights
    final = (
        w.get("gemini", 0.4) * gem.get("likelihood", 50) +
        w.get("vision_brand", 0.4) * brand_score +
        w.get("heuristics", 0.2) * heur.get("risk", 0)
    )

    th = CFG.thresholds
    if final >= th.get("clone", 60):
        decision = "clone"
    elif final >= th.get("suspicious", 30):
        decision = "suspicious"
    else:
        decision = "clean"

    return jsonify({
        "url": url,
        "decision": decision,
        "score": round(final, 1),
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
        "explanation": (
            gem.get("explanation") or
            (f"Detected brand {brand_for_mismatch} on non-canonical domain {reg_domain}."
             if brand_score else "No strong clone indicators.")
        )[:600],
        "errors": {k: v for k, v in {"vision": vision.get("error")}.items() if v}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
