from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import time
import os
from typing import Dict, Any, Optional, Tuple
import json

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
     methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=True)

# Service endpoints
GEMINI_URL = "http://localhost:5003/analyze"
PHISHPEDIA_URL = "http://localhost:5000/analyze"

class CombinedAnalyzer:
    def __init__(self):
        self.weights = {
            "gemini": 0.6,      # AI analysis weight
            "phishpedia": 0.4   # ML analysis weight
        }
    
    def normalize_phishpedia_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Phishpedia response to standardized format"""
        try:
            is_phishing = response.get("isPhishing", False)
            confidence = response.get("confidence", 0.0)
            brand = response.get("brand", "unknown")
            legit_url = response.get("legitUrl", "unknown")
            
            # Convert to 0-100 scale and determine decision
            if is_phishing:
                score = max(70, int(confidence * 100))  # Phishing: 70-100
                decision = "clone"
                advice = f"⚠️ ML model detected {brand} phishing site. Avoid entering credentials."
            elif brand != "unknown" and confidence > 0.3:
                score = min(40, int(confidence * 100))  # Legitimate brand: 0-40
                decision = "clean"
                advice = f"🟢 ML model recognizes legitimate {brand} site."
            else:
                score = 50  # Unknown/uncertain
                decision = "suspicious"
                advice = "🟠 ML model couldn't determine site legitimacy."
            
            return {
                "decision": decision,
                "score": score,
                "confidence": int(confidence * 100),
                "brand": brand,
                "legit_url": legit_url,
                "advice": advice,
                "raw_response": response
            }
        except Exception as e:
            return {
                "decision": "suspicious",
                "score": 50,
                "confidence": 0,
                "brand": "unknown",
                "legit_url": "unknown",
                "advice": f"ML analysis failed: {str(e)}",
                "error": str(e),
                "raw_response": response
            }
    
    def calculate_combined_score(self, gemini_result: Dict, phishpedia_result: Dict) -> Tuple[int, str, str]:
        """Calculate weighted combined score and decision"""
        try:
            # Extract scores
            gemini_score = gemini_result.get("score", 50)
            phishpedia_score = phishpedia_result.get("score", 50)
            
            # Calculate weighted average
            combined_score = (
                self.weights["gemini"] * gemini_score + 
                self.weights["phishpedia"] * phishpedia_score
            )
            
            # Determine consensus
            gemini_decision = gemini_result.get("decision", "suspicious")
            phishpedia_decision = phishpedia_result.get("decision", "suspicious")
            
            # Decision logic
            if gemini_decision == phishpedia_decision:
                # Both agree
                final_decision = gemini_decision
                consensus = "high"
            elif (gemini_decision == "clone" and phishpedia_decision in ["suspicious", "clone"]) or \
                 (phishpedia_decision == "clone" and gemini_decision in ["suspicious", "clone"]):
                # One says clone, other suspicious/clone
                final_decision = "clone"
                combined_score = max(combined_score, 70)  # Boost score for safety
                consensus = "medium"
            elif gemini_decision == "clean" and phishpedia_decision == "clean":
                # Both say clean
                final_decision = "clean"
                consensus = "high"
            else:
                # Disagreement
                final_decision = "suspicious"
                combined_score = max(combined_score, 40)  # Conservative approach
                consensus = "low"
            
            # Generate combined advice
            if final_decision == "clone":
                advice = "⚠️ DANGER: Both AI and ML models indicate this is likely a malicious clone. Do NOT enter any credentials."
            elif final_decision == "clean":
                advice = "🟢 SAFE: Both models indicate this appears to be legitimate. Still verify the URL before entering sensitive information."
            else:
                advice = "🟠 CAUTION: Mixed signals from analysis models. Exercise extreme caution and verify the site independently."
            
            return int(combined_score), final_decision, advice, consensus
            
        except Exception as e:
            return 50, "suspicious", f"Combined analysis failed: {str(e)}", "error"
    
    async def analyze_combined(self, url: Optional[str] = None, image_data: Optional[bytes] = None) -> Dict[str, Any]:
        """Perform combined analysis using both services"""
        results = {
            "gemini": {"status": "pending", "error": None},
            "phishpedia": {"status": "pending", "error": None},
            "combined": {"status": "pending", "error": None}
        }
        
        # Prepare requests
        gemini_success = False
        phishpedia_success = False
        
        # Call Gemini service
        try:
            if image_data:
                # Screenshot analysis
                files = {'screenshot': ('screenshot.png', image_data, 'image/png')}
                data = {'url': url} if url else {}
                gemini_response = requests.post(GEMINI_URL, files=files, data=data, timeout=30)
            else:
                # URL analysis
                gemini_response = requests.post(GEMINI_URL, json={'url': url}, timeout=30)
            
            if gemini_response.status_code == 200:
                results["gemini"] = gemini_response.json()
                results["gemini"]["status"] = "completed"
                gemini_success = True
            else:
                results["gemini"]["error"] = f"HTTP {gemini_response.status_code}"
                results["gemini"]["status"] = "failed"
                
        except Exception as e:
            results["gemini"]["error"] = str(e)
            results["gemini"]["status"] = "failed"
        
        # Call Phishpedia service
        try:
            if image_data:
                # Convert image to base64 for Phishpedia
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                phishpedia_data = {
                    'url': url or '',
                    'screenshot': f'data:image/png;base64,{image_b64}'
                }
            else:
                # For URL-only, we need to let Phishpedia know (it might need screenshot)
                phishpedia_data = {'url': url or ''}
            
            phishpedia_response = requests.post(PHISHPEDIA_URL, json=phishpedia_data, timeout=30)
            
            if phishpedia_response.status_code == 200:
                raw_phishpedia = phishpedia_response.json()
                results["phishpedia"] = self.normalize_phishpedia_response(raw_phishpedia)
                results["phishpedia"]["status"] = "completed"
                phishpedia_success = True
            else:
                results["phishpedia"]["error"] = f"HTTP {phishpedia_response.status_code}"
                results["phishpedia"]["status"] = "failed"
                
        except Exception as e:
            results["phishpedia"]["error"] = str(e)
            results["phishpedia"]["status"] = "failed"
        
        # Calculate combined results
        if gemini_success or phishpedia_success:
            try:
                # Use available results, fallback to defaults for failed services
                gemini_result = results["gemini"] if gemini_success else {"score": 50, "decision": "suspicious"}
                phishpedia_result = results["phishpedia"] if phishpedia_success else {"score": 50, "decision": "suspicious"}
                
                combined_score, final_decision, combined_advice, consensus = self.calculate_combined_score(
                    gemini_result, phishpedia_result
                )
                
                results["combined"] = {
                    "status": "completed",
                    "decision": final_decision,
                    "score": combined_score,
                    "advice": combined_advice,
                    "consensus": consensus,
                    "services_used": {
                        "gemini": gemini_success,
                        "phishpedia": phishpedia_success
                    },
                    "weights": self.weights,
                    "analysis_summary": {
                        "gemini_score": gemini_result.get("score", "N/A"),
                        "phishpedia_score": phishpedia_result.get("score", "N/A"),
                        "agreement": gemini_result.get("decision") == phishpedia_result.get("decision") if gemini_success and phishpedia_success else "N/A"
                    }
                }
                
            except Exception as e:
                results["combined"] = {
                    "status": "failed",
                    "error": f"Combined analysis failed: {str(e)}",
                    "decision": "suspicious",
                    "score": 50,
                    "advice": "Analysis incomplete due to processing error."
                }
        else:
            results["combined"] = {
                "status": "failed",
                "error": "Both services failed",
                "decision": "suspicious", 
                "score": 50,
                "advice": "Unable to analyze - all services unavailable."
            }
        
        return results

# Initialize analyzer
analyzer = CombinedAnalyzer()

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "CipherCop Combined Clone Analysis",
        "version": "1.0.0",
        "endpoints": ["/analyze"],
        "services": {
            "gemini": GEMINI_URL,
            "phishpedia": PHISHPEDIA_URL
        }
    })

@app.route("/analyze", methods=["OPTIONS"])
def analyze_options():
    return "", 200

@app.route("/analyze", methods=["POST"])
def analyze():
    """Combined analysis endpoint"""
    try:
        url = None
        image_data = None
        
        # Parse request
        if request.is_json:
            data = request.get_json() or {}
            url = data.get("url")
        else:
            url = request.form.get("url")
            
        # Handle file upload
        if request.files and "screenshot" in request.files:
            file = request.files["screenshot"]
            if file and file.filename:
                image_data = file.read()
        
        # Validate input
        if not url and not image_data:
            return jsonify({"error": "Either URL or screenshot is required"}), 400
        
        print(f"[COMBINED] Analyzing URL: {url}, Has screenshot: {bool(image_data)}")
        
        # Perform combined analysis
        import asyncio
        results = asyncio.run(analyzer.analyze_combined(url, image_data))
        
        # Add metadata
        results["metadata"] = {
            "timestamp": time.time(),
            "input_type": "screenshot" if image_data else "url",
            "url": url,
            "service": "combined-analysis"
        }
        
        return jsonify(results)
        
    except Exception as e:
        print(f"[COMBINED] Error: {str(e)}")
        return jsonify({
            "error": f"Combined analysis failed: {str(e)}",
            "gemini": {"status": "failed", "error": "Service error"},
            "phishpedia": {"status": "failed", "error": "Service error"},
            "combined": {
                "status": "failed",
                "error": str(e),
                "decision": "suspicious",
                "score": 50,
                "advice": "Analysis failed due to system error."
            }
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    try:
        # Test connectivity to both services
        gemini_ok = False
        phishpedia_ok = False
        
        try:
            resp = requests.get("http://localhost:5003/", timeout=5)
            gemini_ok = resp.status_code == 200
        except:
            pass
            
        try:
            resp = requests.get("http://localhost:5000/", timeout=5)
            phishpedia_ok = resp.status_code == 200
        except:
            pass
        
        return jsonify({
            "status": "healthy",
            "services": {
                "gemini": "online" if gemini_ok else "offline",
                "phishpedia": "online" if phishpedia_ok else "offline"
            },
            "combined_available": gemini_ok or phishpedia_ok
        })
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Combined Clone Analysis Service on port 5002...")
    print(f"Gemini service: {GEMINI_URL}")
    print(f"Phishpedia service: {PHISHPEDIA_URL}")
    app.run(host="0.0.0.0", port=5002, debug=True)