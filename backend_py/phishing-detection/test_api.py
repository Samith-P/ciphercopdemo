import requests
import json

def test_phishing_api():
    """Test the phishing detection API"""
    api_url = "http://localhost:5003/api/phishing/analyze"
    
    # Test URLs
    test_urls = [
        "https://google.com",
        "https://paypal-security-update.fake-domain.com",
        "http://example.com",
        "https://facebook.com"
    ]
    
    print("Testing Phishing Detection API")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        print("-" * 30)
        
        try:
            response = requests.post(
                api_url,
                headers={'Content-Type': 'application/json'},
                json={'url': url},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    result = data['data']
                    print(f"✅ Analysis successful!")
                    print(f"   Threat Level: {result['threatLevel']}")
                    print(f"   Is Phishing: {result['isPhishing']}")
                    print(f"   Risk Score: {result['riskScore']}/100")
                    print(f"   Prediction: {result['prediction']}")
                    if result['flags']:
                        print(f"   Flags: {', '.join(result['flags'])}")
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Could not connect to {api_url}")
            print("   Make sure the Flask service is running on port 5003")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout Error: Request took too long")
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    test_phishing_api()
