import os, json
import google.generativeai as genai

_model = None
def _model_once():
    global _model
    if _model is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: raise RuntimeError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model

PROMPT = (
    "You are a security analyst. Given a webpage screenshot and context, "
    "judge whether it is likely a clone (phishing) of any authorized site.\n"
    "Return a JSON with keys: likelihood (0-100), suspected_brand (string or ''), "
    "explanation (1-3 sentences)."
)

def judge_with_image(image_bytes: bytes, url: str, page_title: str, text_snippet: str, authorized_brands: list[dict]):
    model = _model_once()
    auth_desc = ", ".join(
        f"{b['name']} (domains: {', '.join(b.get('domains', []))})" for b in authorized_brands
    ) or "(none provided)"

    parts = [
        {"text": f"URL: {url}\nTitle: {page_title}\nAuthorized brands: {auth_desc}\nText snippet: {text_snippet[:1200]}"},
        {"mime_type": "image/png", "data": image_bytes},
        {"text": PROMPT},
    ]

    resp = model.generate_content(parts)
    out = resp.text or "{}"
    try: data = json.loads(out)
    except Exception: data = {"likelihood": 50, "suspected_brand": "", "explanation": out[:300]}

    data["likelihood"] = max(0, min(100, int(data.get("likelihood", 50))))
    data["suspected_brand"] = data.get("suspected_brand", "")
    data["explanation"] = data.get("explanation", "")
    return data
