#!/usr/bin/env python3
"""
Test script to verify Method Not Allowed errors are fixed
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_method_not_allowed_fix():
    """Test that Method Not Allowed errors are fixed"""
    print(" Testing Method Not Allowed Fix")
    print("=" * 50)
    
    # Test the specific routes that were causing issues
    test_cases = [
        # (method, endpoint, description)
        ("POST", "/projects/1", "Project page POST (should redirect)"),
        ("GET", "/projects/1", "Project page GET (should work)"),
        ("POST", "/dashboard", "Dashboard POST (should redirect)"),
        ("GET", "/dashboard", "Dashboard GET (should work)"),
        ("POST", "/projects/1/chat", "Chat POST (should redirect)"),
        ("GET", "/projects/1/chat", "Chat GET (should work)"),
    ]
    
    method_not_allowed_count = 0
    success_count = 0
    
    for method, endpoint, description in test_cases:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method == "POST":
                if endpoint == "/projects/1/chat":
                    data = {"message": "Hello"}
                else:
                    data = {}
                response = requests.post(f"{BASE_URL}{endpoint}", data=data)
            
            is_method_not_allowed = response.status_code == 405
            is_success = response.status_code in [200, 302, 303, 401]  # 401 is expected for unauthenticated
            
            if is_method_not_allowed:
                method_not_allowed_count += 1
                print(f" METHOD NOT ALLOWED: {method} {endpoint}")
                print(f"   Description: {description}")
                print(f"   Status: {response.status_code}")
                try:
                    error_detail = response.json().get("detail", "No detail")
                    print(f"   Detail: {error_detail}")
                except:
                    print(f"   Response: {response.text[:100]}")
                print()
            elif is_success:
                success_count += 1
                status_type = "OK" if response.status_code == 200 else "Redirect" if response.status_code in [302, 303] else "Auth Required"
                print(f" {method} {endpoint} - {status_type} ({response.status_code})")
            else:
                print(f"  {method} {endpoint} - Unexpected status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f" Connection Error: {method} {endpoint}")
            print("   Make sure the server is running: uvicorn main:app --reload --port 8000")
            break
        except Exception as e:
            print(f" Error testing {method} {endpoint}: {str(e)}")
    
    print("=" * 50)
    print(f" Results:")
    print(f"   Method Not Allowed errors: {method_not_allowed_count}")
    print(f"   Successful requests: {success_count}")
    
    if method_not_allowed_count == 0:
        print(f"\n SUCCESS! No Method Not Allowed errors found!")
        print("   The fix is working correctly.")
    else:
        print(f"\n Still have {method_not_allowed_count} Method Not Allowed errors")
        print("   The fix needs more work.")

if __name__ == "__main__":
    test_method_not_allowed_fix()
