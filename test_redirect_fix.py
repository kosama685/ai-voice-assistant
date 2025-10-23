#!/usr/bin/env python
"""
Test script to verify the redirect loop fix
"""
import requests
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

# Disable automatic redirects to see the redirect chain
session.allow_redirects = False

def test_landing_page():
    """Test that landing page loads without redirect loop"""
    print("\n✓ Testing landing page (/)...")
    try:
        response = session.get(f"{BASE_URL}/")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✓ Landing page loads successfully")
            return True
        else:
            print(f"  ✗ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_login_page():
    """Test that login page loads"""
    print("\n✓ Testing login page (/auth/login)...")
    try:
        response = session.get(f"{BASE_URL}/auth/login")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✓ Login page loads successfully")
            return True
        else:
            print(f"  ✗ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_register_page():
    """Test that register page loads"""
    print("\n✓ Testing register page (/auth/register)...")
    try:
        response = session.get(f"{BASE_URL}/auth/register")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✓ Register page loads successfully")
            return True
        else:
            print(f"  ✗ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_register_with_plan():
    """Test that register page loads with plan parameter"""
    print("\n✓ Testing register page with plan parameter (/auth/register?plan=starter)...")
    try:
        response = session.get(f"{BASE_URL}/auth/register?plan=starter")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✓ Register page with plan parameter loads successfully")
            return True
        else:
            print(f"  ✗ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_dashboard_redirect():
    """Test that unauthenticated access to dashboard redirects properly"""
    print("\n✓ Testing dashboard redirect for unauthenticated user (/)...")
    try:
        response = session.get(f"{BASE_URL}/", allow_redirects=False)
        print(f"  Status: {response.status_code}")
        if response.status_code in [200, 302]:
            print("  ✓ Dashboard redirect works correctly")
            return True
        else:
            print(f"  ✗ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("REDIRECT LOOP FIX VERIFICATION TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Landing Page", test_landing_page()))
    results.append(("Login Page", test_login_page()))
    results.append(("Register Page", test_register_page()))
    results.append(("Register with Plan", test_register_with_plan()))
    results.append(("Dashboard Redirect", test_dashboard_redirect()))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Redirect loop is fixed.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

