#!/usr/bin/env python3
"""
Startup script for the Chatbot Platform
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    print("🚀 Starting Chatbot Platform...")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    print("📁 Created uploads directory")
    
    # Start the server
    print("🌐 Server starting on http://localhost:8000")
    print("📝 API docs available at http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
