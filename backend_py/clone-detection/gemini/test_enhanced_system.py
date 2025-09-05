#!/usr/bin/env python3
"""
Test the enhanced clone detection system
"""
import requests
import json

def test_enhanced_system():
    """Test the enhanced system with comprehensive analysis stages"""
    
    print("🧪 Testing Enhanced Clone Detection System")
    print("=" * 60)
    
    # Test URL analysis
    test_url = "amazon.com"
    
    print(f"📍 Testing URL: {test_url}")
    print("🔄 Sending request to enhanced analysis endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:5003/analyze",
            data={"url": test_url},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Analysis completed successfully!")
            print(f"🎯 Decision: {result.get('decision', 'Unknown')}")
            print(f"📊 Score: {result.get('score', 'Unknown')}")
            print(f"💡 Advice: {result.get('advice', 'Unknown')}")
            
            # Test enhanced analysis stages
            stages = result.get('analysis_stages', {})
            print("\n🔍 ANALYSIS STAGES BREAKDOWN:")
            print("-" * 40)
            
            for stage_key, stage_data in stages.items():
                stage_name = stage_data.get('name', stage_key)
                status = stage_data.get('status', 'unknown')
                print(f"📋 {stage_name}: {status.upper()}")
                
                key_findings = stage_data.get('key_findings', {})
                if key_findings:
                    print("   Key Findings:")
                    for key, value in key_findings.items():
                        print(f"   - {key}: {value}")
                print()
            
            # Test enhanced Gemini results
            enhanced_gemini = result.get('signals', {}).get('enhanced_gemini', {})
            if enhanced_gemini:
                print("🤖 ENHANCED GEMINI ANALYSIS:")
                print("-" * 30)
                print(f"Final Likelihood: {enhanced_gemini.get('final_likelihood', 'N/A')}%")
                print(f"Confidence: {enhanced_gemini.get('confidence', 'N/A')}%")
                print(f"Final Verdict: {enhanced_gemini.get('final_verdict', 'N/A')}")
                print(f"Threat Indicators: {enhanced_gemini.get('primary_threat_indicators', [])}")
                print(f"Legitimacy Factors: {enhanced_gemini.get('legitimacy_factors', [])}")
                print(f"Expert Explanation: {enhanced_gemini.get('expert_explanation', 'N/A')[:200]}...")
            
            print("\n✅ Enhanced system test completed successfully!")
            
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def check_service_status():
    """Check if the service is running"""
    try:
        response = requests.get("http://localhost:5003/", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if not check_service_status():
        print("❌ Service is not running on port 5003")
        print("💡 Please start the service with: python app.py")
        exit(1)
    
    test_enhanced_system()