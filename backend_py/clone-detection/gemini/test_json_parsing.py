#!/usr/bin/env python3
"""
Test JSON parsing fixes
"""

def test_json_parsing():
    """Test the JSON parsing with the actual Gemini response"""
    
    # This is the actual response from Gemini that was failing
    gemini_response = '''```json
{
  "likelihood": 95,
  "suspected_brand": "Alibaba",
  "explanation": "The analysis reveals a high likelihood of cloning or phishing.  While the website displays Alibaba branding and content consistent with Alibaba.com (e.g., 'The leading B2B ecommerce platform for global trade'),  the absence of detected Alibaba logos despite high-confidence text blocks indicating 'Alibaba.com' is suspicious.  Further, the appearance of similar images on seemingly unrelated sites like Facebook and fina"'''
    
    # Import the function from app.py
    import sys
    sys.path.append('.')
    from app import extract_json_from_text
    
    print("Testing JSON extraction...")
    print(f"Input: {gemini_response[:100]}...")
    
    result = extract_json_from_text(gemini_response)
    print(f"Extracted: {result}")
    
    if result:
        print("✅ SUCCESS!")
        print(f"Likelihood: {result.get('likelihood')}")
        print(f"Suspected Brand: {result.get('suspected_brand')}")
        print(f"Explanation: {result.get('explanation', '')[:100]}...")
    else:
        print("❌ FAILED to extract JSON")

if __name__ == "__main__":
    test_json_parsing()