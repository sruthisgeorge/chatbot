#!/usr/bin/env python3
"""
Test script to verify server can start and routes are properly registered
"""

import sys
import os

def test_server_startup():
    """Test that the server can start without errors"""
    print("🔧 Testing Server Startup")
    print("=" * 40)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Import the main app
        from main import app
        print("✅ Successfully imported main app")
        
        # Check route registration
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append((list(route.methods), route.path))
        
        print(f"📋 Found {len(routes)} routes:")
        
        # Group routes by path to check for conflicts
        route_groups = {}
        for methods, path in routes:
            if path not in route_groups:
                route_groups[path] = []
            route_groups[path].extend(methods)
        
        # Check for potential conflicts
        conflicts = []
        for path, methods in route_groups.items():
            if len(set(methods)) != len(methods):
                conflicts.append((path, methods))
        
        if conflicts:
            print("❌ Route conflicts found:")
            for path, methods in conflicts:
                print(f"   {path}: {methods}")
        else:
            print("✅ No route conflicts found")
        
        # Show some key routes
        key_routes = [
            ("/", ["GET"]),
            ("/login", ["GET", "POST"]),
            ("/register", ["GET", "POST"]),
            ("/dashboard", ["GET", "POST"]),
            ("/projects", ["GET", "POST"]),
            ("/projects/{project_id}", ["GET", "POST"]),
            ("/projects/{project_id}/chat", ["GET", "POST"]),
        ]
        
        print("\n🔍 Checking key routes:")
        for expected_path, expected_methods in key_routes:
            found = False
            for methods, path in routes:
                if path == expected_path:
                    found = True
                    methods_set = set(methods)
                    expected_set = set(expected_methods)
                    if methods_set == expected_set:
                        print(f"✅ {expected_path}: {methods}")
                    else:
                        print(f"⚠️  {expected_path}: {methods} (expected: {expected_methods})")
                    break
            
            if not found:
                print(f"❌ {expected_path}: Not found")
        
        print("\n🎉 Server startup test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_server_startup()
    if not success:
        print("\n💡 Try running: uvicorn main:app --reload --port 8000")
        sys.exit(1)
