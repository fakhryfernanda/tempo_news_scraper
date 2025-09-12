#!/usr/bin/env python3
"""
Test case to document the limitation of accessing premium content
even with authentication on Tempo.co
"""

import subprocess
import sys
import os
import json
import glob

def test_auth_limitation_documentation():
    """Test to document that premium content is not accessible even with authentication"""
    print("Testing documentation of authentication limitation...")
    print("=" * 60)
    
    # Check if AUTH_LIMITATIONS.md exists
    auth_limitations_file = "/home/fakhry/dev/scraper/tempo/AUTH_LIMITATIONS.md"
    if os.path.exists(auth_limitations_file):
        print("✓ AUTH_LIMITATIONS.md documentation file exists")
    else:
        print("✗ AUTH_LIMITATIONS.md documentation file is missing")
        return False
    
    # Check if auth_limitation_demo.py exists
    demo_script = "/home/fakhry/dev/scraper/tempo/scripts/auth_limitation_demo.py"
    if os.path.exists(demo_script):
        print("✓ auth_limitation_demo.py script exists")
    else:
        print("✗ auth_limitation_demo.py script is missing")
        return False
    
    # Check if README.md mentions the limitation
    readme_file = "/home/fakhry/dev/scraper/tempo/README.md"
    if os.path.exists(readme_file):
        with open(readme_file, 'r') as f:
            readme_content = f.read()
            if "Limitations with Premium Content Access" in readme_content:
                print("✓ README.md mentions premium content access limitations")
            else:
                print("✗ README.md does not mention premium content access limitations")
                return False
    else:
        print("✗ README.md file is missing")
        return False
    
    # Check if AGENTS.md mentions the limitation
    agents_file = "/home/fakhry/dev/scraper/tempo/AGENTS.md"
    if os.path.exists(agents_file):
        with open(agents_file, 'r') as f:
            agents_content = f.read()
            if "Limitations with Premium Content Access" in agents_content:
                print("✓ AGENTS.md mentions premium content access limitations")
            else:
                print("✗ AGENTS.md does not mention premium content access limitations")
                return False
    else:
        print("✗ AGENTS.md file is missing")
        return False
    
    print("\n✓ All documentation for authentication limitation is in place")
    return True

def test_help_text_includes_login_option():
    """Test that help text includes the login option"""
    print("\nTesting that help text includes login option...")
    print("-" * 40)
    
    # Test indeks help
    result = subprocess.run(
        ["python", "-m", "src.tempo_scraper", "indeks", "--help"],
        capture_output=True,
        text=True,
        cwd="/home/fakhry/dev/scraper/tempo"
    )
    
    if result.returncode == 0 and "--login" in result.stdout:
        print("✓ Indeks help includes --login option")
    else:
        print("✗ Indeks help does not include --login option")
        return False
    
    # Test article help
    result = subprocess.run(
        ["python", "-m", "src.tempo_scraper", "article", "--help"],
        capture_output=True,
        text=True,
        cwd="/home/fakhry/dev/scraper/tempo"
    )
    
    if result.returncode == 0 and "--login" in result.stdout:
        print("✓ Article help includes --login option")
        return True
    else:
        print("✗ Article help does not include --login option")
        return False

def main():
    """Run all authentication limitation documentation tests"""
    print("Running authentication limitation documentation tests")
    print("=" * 60)
    
    tests = [
        test_auth_limitation_documentation,
        test_help_text_includes_login_option
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
    print("FINAL AUTHENTICATION LIMITATION DOCUMENTATION TEST RESULTS")
    print("=" * 60)
    print(f"Total tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL AUTHENTICATION LIMITATION DOCUMENTATION TESTS PASSED!")
        return True
    else:
        print(f"\n❌ {failed} authentication limitation documentation test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)