#!/usr/bin/env python3
"""
Test script to verify all routes are working correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_route(method, endpoint, expected_status=200, data=None, files=None):
    """Test a single route"""
    try:
        if method.upper() == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method.upper() == "POST":
            if files:
                response = requests.post(f"{BASE_URL}{endpoint}", data=data, files=files)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", data=data)
        elif method.upper() == "PUT":
            response = requests.put(f"{BASE_URL}{endpoint}", data=data)
        elif method.upper() == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}")
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        status_ok = response.status_code == expected_status
        status_icon = "✅" if status_ok else "❌"
        print(f"{status_icon} {method.upper()} {endpoint} - Status: {response.status_code} (Expected: {expected_status})")
        
        if not status_ok and response.status_code != 405:  # 405 is Method Not Allowed
            print(f"   Response: {response.text[:100]}...")
        
        return status_ok
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {method.upper()} {endpoint} - Connection Error (Server not running?)")
        return False
    except Exception as e:
        print(f"❌ {method.upper()} {endpoint} - Error: {str(e)}")
        return False

def test_all_routes():
    """Test all routes to identify Method Not Allowed errors"""
    print("🔍 Testing All Routes")
    print("=" * 50)
    
    # Test basic routes
    print("\n📋 Basic Routes:")
    test_route("GET", "/")
    test_route("GET", "/health")
    test_route("GET", "/login")
    test_route("POST", "/login", data={"email": "test@test.com", "password": "test"})
    test_route("GET", "/register")
    test_route("POST", "/register", data={"email": "test@test.com", "password": "test"})
    test_route("GET", "/logout")
    test_route("POST", "/logout")
    
    # Test protected routes (should return 401 or redirect)
    print("\n🔒 Protected Routes (should return 401 or redirect):")
    test_route("GET", "/dashboard", expected_status=401)
    test_route("GET", "/projects", expected_status=401)
    test_route("POST", "/projects", data={"name": "Test Project"}, expected_status=401)
    test_route("GET", "/projects/1", expected_status=401)
    test_route("POST", "/projects/1/prompts", data={"text": "Test prompt"}, expected_status=401)
    test_route("GET", "/projects/1/prompts", expected_status=401)
    test_route("POST", "/projects/1/chat", data={"message": "Hello"}, expected_status=401)
    test_route("GET", "/projects/1/chat", expected_status=401)
    test_route("POST", "/projects/1/upload", expected_status=401)
    test_route("GET", "/projects/1/files", expected_status=401)
    test_route("GET", "/files/1", expected_status=401)
    test_route("GET", "/api/projects/1/messages", expected_status=401)
    
    # Test API token endpoint
    print("\n🔑 API Token Endpoint:")
    test_route("POST", "/token", data={"username": "test@test.com", "password": "test"}, expected_status=401)
    
    # Test undefined routes
    print("\n❓ Undefined Routes (should return 404 or custom message):")
    test_route("GET", "/undefined-route", expected_status=404)
    test_route("POST", "/undefined-route", expected_status=404)
    test_route("GET", "/api/undefined", expected_status=404)
    
    print("\n" + "=" * 50)
    print("✅ Route testing complete!")
    print("\nIf you see 'Method Not Allowed' errors above, those routes need to be fixed.")
    print("If you see 'Connection Error', make sure the server is running:")
    print("  uvicorn main:app --reload --port 8000")

if __name__ == "__main__":
    test_all_routes()
