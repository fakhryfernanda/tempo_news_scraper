#!/usr/bin/env python3
"""
Integration tests for refactored Tempo.co scraper CLI
"""

import subprocess
import sys
import os
import json
import glob

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\nTesting: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd='/home/fakhry/dev/scraper/tempo'
        )
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Exit code: {result.returncode}")
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def test_refactored_indeks_scraper_basic():
    """Test basic indeks scraper functionality in refactored code"""
    print("Testing basic indeks scraper in refactored code...")
    
    # Test with limited pages and articles
    result = run_command(
        "python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --article-per-page 1",
        "Scrape 1 page with 1 article per page using refactored code"
    )
    
    if result and result.returncode == 0:
        print("✓ Basic indeks scraper test passed for refactored code")
        return True
    else:
        print("✗ Basic indeks scraper test failed for refactored code")
        return False

def test_refactored_article_extractor():
    """Test article extractor functionality in refactored code"""
    print("Testing article extractor in refactored code...")
    
    # Test with a known article URL
    result = run_command(
        "python -m src.tempo_scraper article --url https://www.tempo.co/internasional/demo-nepal-gen-z-bendera-one-piece-2069128",
        "Extract article content using refactored code"
    )
    
    if result and result.returncode == 0:
        print("✓ Article extractor test passed for refactored code")
        # Clean up the output file
        files = glob.glob("/home/fakhry/dev/scraper/tempo/data/output/article_*.json")
        for file in files:
            try:
                os.remove(file)
            except:
                pass
        return True
    else:
        print("✗ Article extractor test failed for refactored code")
        return False

def test_refactored_help():
    """Test help functionality in refactored code"""
    print("Testing help functionality in refactored code...")
    
    # Test main help
    result = run_command(
        "python -m src.tempo_scraper --help",
        "Show main help for refactored code"
    )
    
    if result and result.returncode == 0:
        print("✓ Main help test passed for refactored code")
    else:
        print("✗ Main help test failed for refactored code")
        return False
    
    # Test indeks help
    result = run_command(
        "python -m src.tempo_scraper indeks --help",
        "Show indeks help for refactored code"
    )
    
    if result and result.returncode == 0:
        print("✓ Indeks help test passed for refactored code")
    else:
        print("✗ Indeks help test failed for refactored code")
        return False
    
    # Test article help
    result = run_command(
        "python -m src.tempo_scraper article --help",
        "Show article help for refactored code"
    )
    
    if result and result.returncode == 0:
        print("✓ Article help test passed for refactored code")
        return True
    else:
        print("✗ Article help test failed for refactored code")
        return False

def main():
    """Run all integration tests for refactored code"""
    print("Running integration tests for refactored Tempo.co scraper")
    print("=" * 60)
    
    tests = [
        test_refactored_help,
        test_refactored_indeks_scraper_basic,
        test_refactored_article_extractor
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("FINAL INTEGRATION TEST RESULTS FOR REFACTORED CODE")
    print("=" * 60)
    print(f"Total tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL INTEGRATION TESTS PASSED FOR REFACTORED CODE!")
        return True
    else:
        print(f"\n❌ {failed} integration test(s) failed for refactored code.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)