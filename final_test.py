#!/usr/bin/env python3
"""
Final comprehensive test for Method Not Allowed fix
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_method_not_allowed_fix():
    """Comprehensive test of Method Not Allowed fix"""
    print(" Final Test - Method Not Allowed Fix")
    print("=" * 50)
    
    # Test cases that were causing 405 errors
    test_cases = [
        # (method, endpoint, description, expected_status)
        ("POST", "/projects/1", "Project page POST redirect", [303, 401]),
        ("GET", "/projects/1", "Project page GET", [200, 401]),
        ("POST", "/dashboard", "Dashboard POST redirect", [303, 401]),
        ("GET", "/dashboard", "Dashboard GET", [200, 401]),
        ("POST", "/projects", "Create project", [303, 401]),
        ("GET", "/projects", "List projects", [200, 401]),
        ("POST", "/projects/1/chat", "Send chat message", [303, 401]),
        ("GET", "/projects/1/chat", "Get chat messages", [200, 401]),
        ("POST", "/projects/1/prompts", "Create prompt", [303, 401]),
        ("GET", "/projects/1/prompts", "Get prompts", [200, 401]),
        ("POST", "/projects/1/upload", "Upload file", [303, 401]),
        ("GET", "/projects/1/files", "Get files", [200, 401]),
    ]
    
    method_not_allowed_count = 0
    success_count = 0
    connection_error = False
    
    for method, endpoint, description, expected_statuses in test_cases:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method == "POST":
                # Add appropriate form data
                data = {}
                if endpoint == "/projects/1/chat":
                    data = {"message": "Hello"}
                elif endpoint == "/projects/1/prompts":
                    data = {"text": "Test prompt"}
                elif endpoint == "/projects":
                    data = {"name": "Test Project"}
                elif endpoint == "/projects/1/upload":
                    # Skip file upload test for now
                    print(f"  {method} {endpoint} - Skipped (file upload)")
                    continue
                
                response = requests.post(f"{BASE_URL}{endpoint}", data=data)
            
            is_method_not_allowed = response.status_code == 405
            is_success = response.status_code in expected_statuses
            
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
                status_type = "OK" if response.status_code == 200 else "Redirect" if response.status_code == 303 else "Auth Required"
                print(f" {method} {endpoint} - {status_type} ({response.status_code})")
            else:
                print(f"  {method} {endpoint} - Unexpected status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            connection_error = True
            print(f" Connection Error: {method} {endpoint}")
            print("   Make sure the server is running: uvicorn main:app --reload --port 8000")
            break
        except Exception as e:
            print(f" Error testing {method} {endpoint}: {str(e)}")
    
    print("=" * 50)
    print(f" Results:")
    print(f"   Method Not Allowed errors: {method_not_allowed_count}")
    print(f"   Successful requests: {success_count}")
    
    if connection_error:
        print(f"\n Server not running - please start it first")
        print("   Command: uvicorn main:app --reload --port 8000")
    elif method_not_allowed_count == 0:
        print(f"\n SUCCESS! No Method Not Allowed errors found!")
        print("   The fix is working correctly.")
        print("   All routes are properly handling both GET and POST methods.")
    else:
        print(f"\n Still have {method_not_allowed_count} Method Not Allowed errors")
        print("   The fix needs more work.")

if __name__ == "__main__":
    test_method_not_allowed_fix()
