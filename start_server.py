#!/usr/bin/env python3
"""
Production startup script for Railway deployment.
"""

import os
import uvicorn
from config import Config

def main():
    """Start the FastAPI server with production settings."""
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    # Validate required environment variables
    is_valid, message = Config.validate_openrouter_config()
    if not is_valid:
        print(f"Configuration Error: {message}")
        print("Please set the OPENROUTER_API_KEY environment variable in Railway.")
        exit(1)
    
    print(f"Starting Chatbot Platform on {host}:{port}")
    print(f"Using model: {Config.OPENROUTER_MODEL}")
    print(f"Health check available at: http://{host}:{port}/health")
    
    # Start the server with production settings
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=1,  # Railway handles scaling
        access_log=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()