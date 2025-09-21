#!/usr/bin/env python3
"""
Simple test script to verify authentication is working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_authentication():
    """Test the authentication flow"""
    print("Testing authentication flow...")
    
    # Test registration
    print("\n1. Testing user registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", data=register_data, allow_redirects=False)
        print(f"Registration response status: {response.status_code}")
        
        if response.status_code == 302:  # Redirect to dashboard
            print("✅ Registration successful - redirected to dashboard")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
        return False
    
    # Test login
    print("\n2. Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code == 302:  # Redirect to dashboard
            print("✅ Login successful - redirected to dashboard")
            
            # Check if cookie is set
            cookies = response.cookies
            if 'access_token' in cookies:
                print("✅ Access token cookie is set")
            else:
                print("❌ Access token cookie not found")
                return False
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    
    # Test dashboard access
    print("\n3. Testing dashboard access...")
    try:
        # Use the session to maintain cookies
        session = requests.Session()
        
        # Login first
        login_response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
        
        if login_response.status_code == 302:
            # Try to access dashboard
            dashboard_response = session.get(f"{BASE_URL}/dashboard")
            print(f"Dashboard response status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                print("✅ Dashboard access successful")
                return True
            else:
                print(f"❌ Dashboard access failed: {dashboard_response.status_code}")
                return False
        else:
            print("❌ Login failed during dashboard test")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False

if __name__ == "__main__":
    print("🔐 Authentication Test Script")
    print("=" * 40)
    
    success = test_authentication()
    
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n❌ Authentication tests failed!")
        print("\nTo run the server:")
        print("cd /Users/sruthigeorge/code_base")
        print("uvicorn main:app --reload --port 8000")
