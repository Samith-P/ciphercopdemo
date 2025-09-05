import os, json
from urllib.parse import urlparse
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
    "You are an expert cybersecurity analyst specializing in phishing and website clone detection. "
    "You have been provided with a comprehensive analysis of a webpage including the screenshot, URL, and detailed Google Vision AI results.\n\n"
    
    "ANALYSIS DATA PROVIDED:\n"
    "1. 📍 URL of the webpage\n"
    "2. 🏷️ Brand logos detected with confidence scores\n"
    "3. 📝 All text extracted from the page\n"
    "4. 🌐 Web entities (what Google recognizes this image as)\n"
    "5. 🔍 Similar images found across the web\n"
    "6. 📄 Other websites using similar/identical images\n"
    "7. 🎯 Objects detected in the image\n"
    "8. 🏷️ Image classification labels\n"
    "9. 🛡️ Google's spoof detection results\n"
    "10. 👤 Human elements detected\n"
    "11. 📊 Text confidence analysis\n"
    "12. 🏢 List of authorized legitimate brands and their domains\n\n"
    
    "CLONE DETECTION ANALYSIS:\n"
    "Analyze this webpage for potential cloning/phishing using these critical factors:\n\n"
    
    "🔍 DOMAIN ANALYSIS:\n"
    "- Does the URL domain match legitimate domains for any detected brands?\n"
    "- Are there suspicious domain variations (typosquatting, subdomain abuse)?\n"
    "- Is the domain trying to impersonate a well-known brand?\n\n"
    
    "🏷️ BRAND CONSISTENCY:\n"
    "- Do detected logos match the domain?\n"
    "- Are there brand logos that don't belong to the domain owner?\n"
    "- Are multiple competing brands shown together (red flag)?\n\n"
    
    "🌐 WEB INTELLIGENCE:\n"
    "- Do similar images appear on legitimate vs suspicious sites?\n"
    "- What do web entities suggest about this content?\n"
    "- Are there patterns indicating content theft?\n\n"
    
    "📝 CONTENT ANALYSIS:\n"
    "- Does extracted text match the supposed brand/service?\n"
    "- Are there spelling errors, poor grammar, or suspicious phrases?\n"
    "- Do login forms or sensitive data requests match the domain?\n\n"
    
    "🛡️ TECHNICAL INDICATORS:\n"
    "- What does Google's spoof detection indicate?\n"
    "- Are there technical inconsistencies?\n"
    "- Do objects/labels suggest legitimate vs fake content?\n\n"
    
    "Return a JSON response with:\n"
    "{\n"
    "  \"likelihood\": 0-100 (clone probability),\n"
    "  \"suspected_brand\": \"brand name or empty string\",\n"
    "  \"explanation\": \"Detailed 3-5 sentence analysis explaining your reasoning, citing specific evidence from the Vision AI data\"\n"
    "}\n\n"
    
    "Be thorough and cite specific evidence from the provided Vision AI analysis in your explanation."
)

def judge_with_image(image_bytes: bytes, url: str, page_title: str, text_snippet: str, authorized_brands: list[dict], vision_results: dict = None):
    model = _model_once()
    auth_desc = ", ".join(
        f"{b['name']} (domains: {', '.join(b.get('domains', []))})" for b in authorized_brands
    ) or "(none provided)"

    # Prepare comprehensive Vision AI results summary
    vision_summary = ""
    if vision_results:
        # 1. Detected Logos/Brands
        detected_logos = vision_results.get("logos", [])
        if detected_logos:
            logo_summary = ", ".join([f"{logo['description']} (confidence: {logo['score']:.2f})" for logo in detected_logos])
            vision_summary += f"🏷️ Detected Brands/Logos: {logo_summary}\n"
        else:
            vision_summary += "🏷️ Detected Brands/Logos: None\n"
        
        # 2. Extracted Text
        extracted_text = vision_results.get("text", "")
        if extracted_text:
            text_preview = extracted_text[:600] + "..." if len(extracted_text) > 600 else extracted_text
            vision_summary += f"📝 Extracted Text: {text_preview}\n"
        else:
            vision_summary += "📝 Extracted Text: None\n"
        
        # 3. Web Entities (what the image represents)
        web_entities = vision_results.get("web_entities", [])
        if web_entities:
            entities_summary = ", ".join([f"{entity['description']} ({entity['score']:.2f})" for entity in web_entities[:5]])
            vision_summary += f"🌐 Web Entities: {entities_summary}\n"
        
        # 4. Similar Images Found
        similar_images = vision_results.get("similar_images", [])
        if similar_images:
            vision_summary += f"🔍 Similar Images Found: {len(similar_images)} matches on the web\n"
        
        # 5. Pages with Matching Images
        matching_pages = vision_results.get("pages_with_matching_images", [])
        if matching_pages:
            page_domains = []
            for page in matching_pages[:3]:  # Show top 3
                if page.get("url"):
                    try:
                        domain = urlparse(page["url"]).netloc
                        page_domains.append(domain)
                    except:
                        pass
            if page_domains:
                vision_summary += f"📄 Pages with Similar Images: {', '.join(page_domains)}\n"
        
        # 6. Detected Objects
        detected_objects = vision_results.get("detected_objects", [])
        if detected_objects:
            objects_summary = ", ".join([f"{obj['name']} ({obj['score']:.2f})" for obj in detected_objects[:5]])
            vision_summary += f"🎯 Detected Objects: {objects_summary}\n"
        
        # 7. Image Labels/Classification
        labels = vision_results.get("labels", [])
        if labels:
            labels_summary = ", ".join([f"{label['description']} ({label['score']:.2f})" for label in labels[:5]])
            vision_summary += f"🏷️ Image Categories: {labels_summary}\n"
        
        # 8. Safe Search Results
        safe_search = vision_results.get("safe_search", {})
        if safe_search:
            spoof_level = safe_search.get("spoof", "UNKNOWN")
            vision_summary += f"🛡️ Spoof Detection: {spoof_level}\n"
        
        # 9. Face Detection
        faces = vision_results.get("detected_faces", [])
        if faces:
            vision_summary += f"👤 Human Faces Detected: {len(faces)}\n"
        
        # 10. Text Blocks with Confidence
        text_blocks = vision_results.get("text_blocks", [])
        high_confidence_text = [block for block in text_blocks if block.get("confidence", 0) > 0.8]
        if high_confidence_text:
            vision_summary += f"📊 High-Confidence Text Blocks: {len(high_confidence_text)}\n"
    else:
        vision_summary = "❌ Vision AI analysis not available\n"

    # Enhanced context with comprehensive Vision AI results
    context_text = (
        f"🌐 TARGET URL: {url}\n"
        f"📋 PAGE TITLE: {page_title}\n"
        f"🏢 AUTHORIZED BRANDS: {auth_desc}\n\n"
        f"📊 COMPREHENSIVE GOOGLE VISION AI ANALYSIS:\n"
        f"{vision_summary}\n"
        f"📄 ADDITIONAL PAGE CONTENT:\n{text_snippet[:500]}{'...' if len(text_snippet) > 500 else ''}\n\n"
        f"⚡ ANALYSIS INSTRUCTIONS:\n"
        f"Based on all the above data, perform a comprehensive clone detection analysis. "
        f"Pay special attention to domain-brand mismatches, suspicious content patterns, "
        f"and any evidence of impersonation or content theft."
    )

    parts = [
        {"text": context_text},
        {"mime_type": "image/png", "data": image_bytes},
        {"text": PROMPT},
    ]

    resp = model.generate_content(parts)
    out = resp.text or "{}"
    try: data = json.loads(out)
    except Exception: data = {"likelihood": 50, "suspected_brand": "", "explanation": out[:500]}

    data["likelihood"] = max(0, min(100, int(data.get("likelihood", 50))))
    data["suspected_brand"] = data.get("suspected_brand", "")
    data["explanation"] = data.get("explanation", "")
    return data


def enhanced_gemini_analysis(image_bytes: bytes, url: str, vision_results: dict, initial_gemini: dict, brand_analysis: dict, heuristic_results: dict):
    """
    Enhanced Gemini analysis that takes all previous analysis results and provides final assessment
    """
    model = _model_once()
    
    # Prepare comprehensive analysis summary
    analysis_summary = f"""
🔍 COMPREHENSIVE ANALYSIS SUMMARY:

📍 TARGET URL: {url or 'Screenshot-only analysis'}

🤖 INITIAL GEMINI AI ASSESSMENT:
- Likelihood: {initial_gemini.get('likelihood', 'N/A')}%
- Suspected Brand: {initial_gemini.get('suspected_brand', 'None')}
- Reasoning: {initial_gemini.get('explanation', 'N/A')[:300]}...

🏷️ BRAND ANALYSIS RESULTS:
- Detected Brand: {brand_analysis.get('detected_brand', 'None')}
- Legitimate Domains: {', '.join(brand_analysis.get('allowed_domains', []))}
- Domain Match: {'✅ Legitimate' if brand_analysis.get('is_legitimate_match') else '❌ Suspicious/Unknown'}
- Brand Mismatch Score: {brand_analysis.get('brand_score', 0)}
- Analysis Type: {'URL + Screenshot' if url else 'Screenshot Only'}

🔧 HEURISTIC ANALYSIS:
- Domain Risk Score: {heuristic_results.get('risk', 0)}
- Registered Domain: {heuristic_results.get('registered_domain', 'Unknown')}
- Suspicious Patterns: {len(heuristic_results.get('signals', {}))} detected

🌐 GOOGLE VISION AI FINDINGS:
"""
    
    # Add Vision AI summary
    if vision_results.get("logos"):
        logos_info = ", ".join([f"{logo['description']} ({logo['score']:.2f})" for logo in vision_results["logos"]])
        analysis_summary += f"- Detected Logos: {logos_info}\n"
    
    if vision_results.get("web_entities"):
        entities_info = ", ".join([f"{entity['description']}" for entity in vision_results["web_entities"][:3]])
        analysis_summary += f"- Web Entities: {entities_info}\n"
    
    if vision_results.get("pages_with_matching_images"):
        matching_count = len(vision_results["pages_with_matching_images"])
        analysis_summary += f"- Similar Images Found: {matching_count} matches across the web\n"
    
    if vision_results.get("safe_search", {}).get("spoof"):
        spoof_level = vision_results["safe_search"]["spoof"]
        analysis_summary += f"- Google Spoof Detection: {spoof_level}\n"

    enhanced_prompt = f"""
You are a senior cybersecurity analyst conducting a FINAL ASSESSMENT of a potential phishing/clone website.

You have been provided with comprehensive multi-stage analysis results from:
1. Google Vision AI (logo detection, content analysis)
2. Initial Gemini AI assessment 
3. Brand legitimacy verification
4. Heuristic pattern analysis

{analysis_summary}

CRITICAL ASSESSMENT TASK:
Based on ALL the evidence above, provide your FINAL expert judgment on whether this is a legitimate website or a phishing/clone attempt.

Consider these key factors:
🔍 DOMAIN-BRAND CONSISTENCY: Does the URL match the detected brand's legitimate domains?
🏷️ LOGO AUTHENTICITY: Are brand logos being used legitimately or stolen?
🌐 WEB INTELLIGENCE: Do similar images appear on suspicious vs legitimate sites?
📊 PATTERN ANALYSIS: Do heuristic signals indicate suspicious behavior?
🤖 AI CONSENSUS: Do multiple AI systems agree on the threat level?

IMPORTANT: If the URL domain matches the detected brand's legitimate domains AND the visual content is consistent, this should be classified as LEGITIMATE with low likelihood scores (0-20). Only flag as suspicious/phishing when there are clear mismatches or red flags.

Provide your response in JSON format:
{{
  "final_likelihood": 0-100 (final clone/phishing probability),
  "confidence": 0-100 (how confident you are in this assessment),
  "primary_threat_indicators": ["list", "of", "main", "red", "flags"],
  "legitimacy_factors": ["list", "of", "factors", "suggesting", "legitimacy"],
  "final_verdict": "LEGITIMATE|SUSPICIOUS|PHISHING",
  "expert_explanation": "Comprehensive 4-6 sentence explanation of your final decision, citing specific evidence from all analysis stages"
}}

Be decisive and thorough. This is the final assessment that will determine user safety.
"""

    parts = [
        {"text": enhanced_prompt},
        {"mime_type": "image/png", "data": image_bytes}
    ]

    try:
        resp = model.generate_content(parts)
        out = resp.text or "{}"
        
        # Try to extract JSON from the response (similar to initial Gemini)
        try: 
            # First try direct JSON parsing
            data = json.loads(out)
        except Exception:
            # Try to extract JSON from text (handle code fences)
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            try:
                from app import extract_json_from_text
                extracted = extract_json_from_text(out)
            except ImportError:
                # Fallback JSON extraction if import fails
                import re
                json_match = re.search(r'\{.*\}', out, re.DOTALL)
                if json_match:
                    try:
                        extracted = json.loads(json_match.group())
                    except:
                        extracted = None
                else:
                    extracted = None
            if extracted:
                data = {
                    "final_likelihood": extracted.get("final_likelihood", initial_gemini.get("likelihood", 50)),
                    "confidence": extracted.get("confidence", 70),
                    "primary_threat_indicators": extracted.get("primary_threat_indicators", ["Extracted from partial response"]),
                    "legitimacy_factors": extracted.get("legitimacy_factors", []),
                    "final_verdict": extracted.get("final_verdict", "SUSPICIOUS"),
                    "expert_explanation": extracted.get("expert_explanation", out[:500] if out else "Enhanced analysis failed")
                }
            else:
                data = {
                    "final_likelihood": initial_gemini.get("likelihood", 50),
                    "confidence": 70,
                    "primary_threat_indicators": ["JSON parsing failed"],
                    "legitimacy_factors": [],
                    "final_verdict": "SUSPICIOUS",
                    "expert_explanation": out[:500] if out else "Enhanced analysis failed"
                }

        # Ensure proper data types and bounds
        data["final_likelihood"] = max(0, min(100, int(data.get("final_likelihood", 50))))
        data["confidence"] = max(0, min(100, int(data.get("confidence", 70))))
        data["primary_threat_indicators"] = data.get("primary_threat_indicators", [])
        data["legitimacy_factors"] = data.get("legitimacy_factors", [])
        data["final_verdict"] = data.get("final_verdict", "SUSPICIOUS")
        data["expert_explanation"] = data.get("expert_explanation", "")
        
        return data
        
    except Exception as e:
        return {
            "final_likelihood": initial_gemini.get("likelihood", 50),
            "confidence": 30,
            "primary_threat_indicators": [f"Enhanced analysis failed: {str(e)}"],
            "legitimacy_factors": [],
            "final_verdict": "SUSPICIOUS",
            "expert_explanation": f"Enhanced Gemini analysis encountered an error: {str(e)}"
        }
