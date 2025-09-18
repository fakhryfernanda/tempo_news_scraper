#!/usr/bin/env python3
"""
Complete test suite runner for Tempo.co scraper
"""

import subprocess
import sys
import os

def run_test_script(script_name, description):
    """Run a test script and return success status"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ["python", script_name],
            cwd="/home/fakhry/dev/scraper/tempo",
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} PASSED")
            return True
        else:
            print(f"✗ {description} FAILED")
            return False
            
    except Exception as e:
        print(f"✗ {description} FAILED with exception: {e}")
        return False

def main():
    """Run all test suites"""
    print("Running complete test suite for Tempo.co scraper")
    print("=" * 60)
    
    test_scripts = [
        ("tests/test_comprehensive.py", "Comprehensive Unit Tests"),
        ("tests/test_integration.py", "Integration Tests"),
        ("tests/test_article_extractor.py", "Article Extractor Unit Tests"),
        ("tests/test_categorization.py", "Categorization Feature Tests")
    ]
    
    passed = 0
    failed = 0
    
    for script, description in test_scripts:
        if os.path.exists(os.path.join("/home/fakhry/dev/scraper/tempo", script)):
            if run_test_script(script, description):
                passed += 1
            else:
                failed += 1
        else:
            print(f"Skipping {description} - script not found: {script}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Total test suites: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The Tempo.co scraper is working correctly.")
        return 0
    else:
        print(f"\n❌ {failed} test suite(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())