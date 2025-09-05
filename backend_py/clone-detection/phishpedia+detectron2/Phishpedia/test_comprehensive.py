#!/usr/bin/env python3
"""
Comprehensive testing script for Phishpedia with proper test cases
"""
import os
import time
from datetime import datetime
from phishpedia import PhishpediaWrapper

def test_single_case(phishpedia_cls, case_name, url, screenshot_path, expected_result=None):
    """Test a single case and return results"""
    print(f"\n🧪 Testing: {case_name}")
    print(f"📄 URL: {url}")
    print(f"🖼️  Screenshot: {screenshot_path}")
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        return None
    
    start_time = time.time()
    
    try:
        phish_category, pred_target, matched_domain, plotvis, siamese_conf, pred_boxes, logo_recog_time, logo_match_time = \
            phishpedia_cls.test_orig_phishpedia(url, screenshot_path, None)
        
        total_time = time.time() - start_time
        
        # Determine result
        if phish_category == 0:
            result = 'BENIGN' if pred_target is None else 'BENIGN (brand detected but domain consistent)'
        else:
            result = 'PHISHING'
        
        # Create result summary
        test_result = {
            'case_name': case_name,
            'url': url,
            'result': result,
            'phish_category': phish_category,
            'predicted_brand': pred_target,
            'matched_domains': matched_domain,
            'confidence': siamese_conf,
            'logo_count': len(pred_boxes) if pred_boxes is not None else 0,
            'detection_time': round(total_time, 3),
            'logo_recog_time': round(logo_recog_time, 3),
            'logo_match_time': round(logo_match_time, 3),
            'expected': expected_result,
            'correct': expected_result is None or (expected_result.upper() in result.upper())
        }
        
        # Print summary
        print(f"🎯 Result: {result}")
        if pred_target:
            print(f"🏷️  Brand: {pred_target} (confidence: {siamese_conf:.4f})")
            print(f"🌐 Domains: {matched_domain}")
        print(f"⏱️  Time: {total_time:.3f}s (detection: {logo_recog_time:.3f}s + matching: {logo_match_time:.3f}s)")
        
        if expected_result:
            status = "✅ CORRECT" if test_result['correct'] else "❌ INCORRECT"
            print(f"📊 Expected: {expected_result} | {status}")
        
        return test_result
        
    except Exception as e:
        print(f"❌ Error testing {case_name}: {e}")
        return None

def run_test_suite():
    """Run comprehensive test suite"""
    print("🚀 PHISHPEDIA COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Initialize Phishpedia
    print("🔧 Initializing Phishpedia...")
    phishpedia_cls = PhishpediaWrapper()
    
    # Define test cases (you'll need to add proper screenshots)
    test_cases = [
        # Format: (case_name, url, screenshot_path, expected_result)
        ("legitimate_amazon", "https://amazon.com", "test_screenshots/amazon_real.png", "BENIGN"),
        ("legitimate_alibaba", "https://alibaba.com", "test_screenshots/alibaba_real.png", "BENIGN"),
        ("phishing_amazon", "https://amazon1.com", "test_screenshots/amazon_fake.png", "PHISHING"),
        ("phishing_alibaba", "https://alibaba-secure.net", "test_screenshots/alibaba_fake.png", "PHISHING"),
        ("regional_amazon", "https://amazon.co.uk", "test_screenshots/amazon_uk.png", "BENIGN"),
        ("no_logos", "https://example.com", "test_screenshots/no_logos.png", "BENIGN"),
    ]
    
    results = []
    correct_predictions = 0
    total_tests = 0
    
    print(f"\n📋 Running {len(test_cases)} test cases...")
    
    for case_name, url, screenshot_path, expected in test_cases:
        result = test_single_case(phishpedia_cls, case_name, url, screenshot_path, expected)
        if result:
            results.append(result)
            total_tests += 1
            if result['correct']:
                correct_predictions += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if total_tests > 0:
        accuracy = (correct_predictions / total_tests) * 100
        print(f"🎯 Accuracy: {correct_predictions}/{total_tests} ({accuracy:.1f}%)")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for result in results:
            status = "✅" if result['correct'] else "❌"
            print(f"  {status} {result['case_name']}: {result['result']} ({result['detection_time']}s)")
            if result['predicted_brand']:
                print(f"      Brand: {result['predicted_brand']} ({result['confidence']:.3f})")
    
    # Performance stats
    if results:
        avg_time = sum(r['detection_time'] for r in results) / len(results)
        print(f"\n⏱️  Average detection time: {avg_time:.3f}s")
        
        # Brand detection stats
        brands_detected = [r for r in results if r['predicted_brand']]
        print(f"🏷️  Brand detection rate: {len(brands_detected)}/{len(results)} ({len(brands_detected)/len(results)*100:.1f}%)")
    
    return results

def create_test_screenshots_guide():
    """Create a guide for setting up test screenshots"""
    guide = """
📸 TEST SCREENSHOTS SETUP GUIDE
================================

To run comprehensive tests, create these screenshot files:

1. test_screenshots/amazon_real.png
   - Screenshot of real amazon.com homepage
   - Should contain Amazon logo

2. test_screenshots/alibaba_real.png
   - Screenshot of real alibaba.com homepage
   - Should contain Alibaba logo

3. test_screenshots/amazon_fake.png
   - Screenshot with Amazon logo but from fake site
   - Use for testing phishing detection

4. test_screenshots/alibaba_fake.png
   - Screenshot with Alibaba logo but from fake site
   - Use for testing phishing detection

5. test_screenshots/amazon_uk.png
   - Screenshot of amazon.co.uk (regional)
   - Should be detected as benign

6. test_screenshots/no_logos.png
   - Screenshot with no recognizable brand logos
   - Should be detected as benign

📁 Create directory: mkdir test_screenshots
🌐 Take screenshots using browser dev tools or screenshot tools
📏 Recommended size: 1920x1080 or similar
💾 Save as PNG format
"""
    
    print(guide)
    
    # Create directory
    os.makedirs("test_screenshots", exist_ok=True)
    print("✅ Created test_screenshots directory")

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        create_test_screenshots_guide()
        return
    
    # Check if test screenshots exist
    if not os.path.exists("test_screenshots"):
        print("❌ Test screenshots directory not found!")
        print("Run: python test_comprehensive.py --setup")
        return
    
    # Run tests
    results = run_test_suite()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"test_results_{timestamp}.txt"
    
    with open(results_file, 'w') as f:
        f.write("Phishpedia Test Results\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        for result in results:
            f.write(f"Case: {result['case_name']}\n")
            f.write(f"URL: {result['url']}\n")
            f.write(f"Result: {result['result']}\n")
            f.write(f"Brand: {result['predicted_brand']}\n")
            f.write(f"Confidence: {result['confidence']}\n")
            f.write(f"Time: {result['detection_time']}s\n")
            f.write("-" * 30 + "\n")
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main()