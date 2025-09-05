#!/usr/bin/env python3
"""
Create proper test cases with matching screenshots and URLs
"""
import os
import shutil
from datetime import datetime

def create_test_case(test_dir, case_name, url, screenshot_source=None):
    """Create a test case directory with info.txt and shot.png"""
    case_path = os.path.join(test_dir, case_name)
    os.makedirs(case_path, exist_ok=True)
    
    # Write URL to info.txt
    with open(os.path.join(case_path, 'info.txt'), 'w') as f:
        f.write(url)
    
    # Copy screenshot if provided
    if screenshot_source and os.path.exists(screenshot_source):
        shutil.copy2(screenshot_source, os.path.join(case_path, 'shot.png'))
        print(f"✅ Created test case: {case_name}")
        print(f"   URL: {url}")
        print(f"   Screenshot: copied from {screenshot_source}")
    else:
        print(f"⚠️  Created test case: {case_name} (no screenshot)")
        print(f"   URL: {url}")
        print(f"   Note: Add shot.png manually")
    
    return case_path

def main():
    # Create test directory
    test_dir = "datasets/test_cases_proper"
    os.makedirs(test_dir, exist_ok=True)
    
    print("🔧 Creating proper test cases...")
    print("=" * 60)
    
    # Test cases with proper URL-screenshot matching
    test_cases = [
        # Legitimate cases
        ("amazon_legit", "https://amazon.com", None),
        ("alibaba_legit", "https://alibaba.com", None),
        ("google_legit", "https://google.com", None),
        
        # Phishing cases (suspicious domains with brand logos)
        ("amazon_phish_1", "https://amazon-security.com", None),
        ("amazon_phish_2", "https://amazon1.com", None),
        ("alibaba_phish_1", "https://alibaba-trade.net", None),
        ("google_phish_1", "https://google-verify.com", None),
        
        # Edge cases
        ("amazon_regional", "https://amazon.co.uk", None),  # Should be benign
        ("amazon_subdomain", "https://aws.amazon.com", None),  # Should be benign
    ]
    
    for case_name, url, screenshot in test_cases:
        create_test_case(test_dir, case_name, url, screenshot)
    
    print("=" * 60)
    print("📋 NEXT STEPS:")
    print("1. Add proper screenshots to each test case folder")
    print("2. Run tests with: python phishpedia.py --folder datasets/test_cases_proper")
    print("3. Screenshots should match the URL content (Amazon screenshot for Amazon URL)")
    print(f"\n📁 Test directory created: {test_dir}")

if __name__ == "__main__":
    main()