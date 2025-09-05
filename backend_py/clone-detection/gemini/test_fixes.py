#!/usr/bin/env python3
"""
Test script to verify the clone detection fixes
"""
import requests
import json

def check_service_running():
    """Check if the service is running"""
    try:
        response = requests.get("http://localhost:5003/", timeout=5)
        return True
    except:
        return False

def test_url_analysis():
    """Test URL analysis with screenshot automation"""
    
    # First check if service is running
    if not check_service_running():
        print("❌ Service is not running on port 5003!")
        print("💡 Start the service first: python app.py")
        return
    
    url = "http://localhost:5003/analyze"
    
    # Test with a URL that should trigger screenshot automation
    test_data = {
        "url": "amazon.com"  # Test without https:// to check normalization
    }
    
    print("✅ Service is running on port 5003")
    print("Testing URL analysis with screenshot automation...")
    print(f"Sending request to: {url}")
    print(f"Test data: {test_data}")
    
    try:
        response = requests.post(url, json=test_data, timeout=120)  # Increased timeout
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Decision: {result.get('decision')}")
            print(f"Score: {result.get('score')}")
            print(f"Advice: {result.get('advice')}")
            
            # Check if Gemini analysis worked
            gemini_signals = result.get('signals', {}).get('gemini', {})
            print(f"Gemini likelihood: {gemini_signals.get('likelihood')}")
            print(f"Suspected brand: {gemini_signals.get('suspected_brand')}")
            
            # Check breakdown
            breakdown = result.get('breakdown', {})
            print(f"Scoring breakdown: {breakdown}")
            
            # Check if screenshot was taken
            if result.get('signals', {}).get('vision', {}).get('logos'):
                print(f"✅ Screenshot automation worked - detected logos!")
            else:
                print("⚠️ No logos detected - check screenshot automation")
            
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_screenshot_upload():
    """Test screenshot upload functionality"""
    print("\n" + "="*50)
    print("Testing screenshot upload (if you have a test image)...")
    print("This test is optional - requires a test image file")
    print("="*50)

if __name__ == "__main__":
    test_url_analysis()
    test_screenshot_upload()