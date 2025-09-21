#!/usr/bin/env python3
"""
Quick test to verify Method Not Allowed fix
"""

import requests

BASE_URL = "http://localhost:8000"

def quick_test():
    """Quick test of the problematic routes"""
    print("🔧 Quick Test - Method Not Allowed Fix")
    print("=" * 40)
    
    # Test the specific route that was failing
    try:
        # This should NOT return 405 Method Not Allowed
        response = requests.post(f"{BASE_URL}/projects/1")
        print(f"POST /projects/1 - Status: {response.status_code}")
        
        if response.status_code == 405:
            print("❌ STILL GETTING 405 Method Not Allowed!")
            try:
                error = response.json()
                print(f"   Error: {error}")
            except:
                print(f"   Response: {response.text}")
        elif response.status_code in [303, 302, 401]:
            print("✅ SUCCESS! No more 405 error")
            print(f"   Got expected status: {response.status_code}")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Server not running?")
        print("   Run: uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()
