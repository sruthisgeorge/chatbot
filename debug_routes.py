#!/usr/bin/env python3
"""
Debug script to identify Method Not Allowed errors
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_specific_routes():
    """Test specific routes that might be causing Method Not Allowed errors"""
    print("Testing Specific Routes for Method Not Allowed Errors")
    print("=" * 60)
    
    # Test routes that commonly cause Method Not Allowed errors
    test_cases = [
        # (method, endpoint, expected_status, description)
        ("GET", "/", 302, "Root redirect"),
        ("GET", "/health", 200, "Health check"),
        ("GET", "/login", 200, "Login page"),
        ("POST", "/login", 401, "Login form (no auth)"),
        ("GET", "/register", 200, "Register page"),
        ("POST", "/register", 302, "Register form"),
        ("GET", "/dashboard", 401, "Dashboard (no auth)"),
        ("GET", "/projects", 401, "List projects (no auth)"),
        ("POST", "/projects", 401, "Create project (no auth)"),
        ("GET", "/projects/1", 401, "Get project (no auth)"),
        ("POST", "/projects/1/prompts", 401, "Create prompt (no auth)"),
        ("GET", "/projects/1/prompts", 401, "Get prompts (no auth)"),
        ("POST", "/projects/1/chat", 401, "Send chat (no auth)"),
        ("GET", "/projects/1/chat", 401, "Get chat (no auth)"),
        ("POST", "/projects/1/upload", 401, "Upload file (no auth)"),
        ("GET", "/projects/1/files", 401, "Get files (no auth)"),
        ("GET", "/files/1", 401, "Download file (no auth)"),
        ("GET", "/api/projects/1/messages", 401, "API messages (no auth)"),
        ("POST", "/token", 401, "Token endpoint (no auth)"),
    ]
    
    method_not_allowed_count = 0
    other_errors = 0
    
    for method, endpoint, expected_status, description in test_cases:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method == "POST":
                if endpoint == "/login":
                    data = {"email": "test@test.com", "password": "test"}
                elif endpoint == "/register":
                    data = {"email": "test@test.com", "password": "test"}
                elif endpoint == "/projects":
                    data = {"name": "Test Project"}
                elif endpoint == "/projects/1/prompts":
                    data = {"text": "Test prompt"}
                elif endpoint == "/projects/1/chat":
                    data = {"message": "Hello"}
                elif endpoint == "/token":
                    data = {"username": "test@test.com", "password": "test"}
                else:
                    data = {}
                response = requests.post(f"{BASE_URL}{endpoint}", data=data)
            else:
                continue
            
            status_ok = response.status_code == expected_status
            is_method_not_allowed = response.status_code == 405
            
            if is_method_not_allowed:
                method_not_allowed_count += 1
                print(f"METHOD NOT ALLOWED: {method} {endpoint}")
                print(f"   Expected: {expected_status}, Got: {response.status_code}")
                print(f"   Description: {description}")
                try:
                    error_detail = response.json().get("detail", "No detail")
                    print(f"   Detail: {error_detail}")
                except:
                    print(f"   Response: {response.text[:100]}")
                print()
            elif not status_ok:
                other_errors += 1
                print(f"WARNING: {method} {endpoint} - Status: {response.status_code} (Expected: {expected_status})")
                print(f"   Description: {description}")
            else:
                print(f"OK: {method} {endpoint} - OK")
                
        except requests.exceptions.ConnectionError:
            print(f"Connection Error: {method} {endpoint}")
            print("   Make sure the server is running: uvicorn main:app --reload --port 8000")
            break
        except Exception as e:
            print(f"Error testing {method} {endpoint}: {str(e)}")
    
    print("=" * 60)
    print(f"Results:")
    print(f"   Method Not Allowed errors: {method_not_allowed_count}")
    print(f"   Other errors: {other_errors}")
    
    if method_not_allowed_count > 0:
        print(f"\nFix needed: {method_not_allowed_count} routes have Method Not Allowed errors")
        print("   These routes need proper HTTP method definitions")
    else:
        print(f"\nNo Method Not Allowed errors found!")

if __name__ == "__main__":
    test_specific_routes()
