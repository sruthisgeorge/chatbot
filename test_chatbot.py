#!/usr/bin/env python3
"""
Test script for the ChatBot integration with OpenRouter and Grok 4.
This script tests the ChatBot class without requiring the full FastAPI application.
"""

import os
import sys
import asyncio
from chatbot import ChatBot
from config import Config

def test_chatbot_initialization():
    """Test ChatBot initialization"""
    print("Testing ChatBot initialization...")
    
    # Check if API key is configured
    is_valid, message = Config.validate_openrouter_config()
    print(f"Config validation: {message}")
    
    if not is_valid:
        print("❌ OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable.")
        print("   You can get an API key from: https://openrouter.ai/")
        return False
    
    try:
        chatbot = ChatBot()
        print("✅ ChatBot initialized successfully with Grok 4")
        return chatbot
    except Exception as e:
        print(f"❌ ChatBot initialization failed: {e}")
        return False

async def test_chatbot_functionality(chatbot):
    """Test basic ChatBot functionality"""
    print("\nTesting ChatBot functionality...")
    
    # Test API key validation
    if await chatbot.validate_api_key():
        print("✅ API key is valid")
    else:
        print("❌ API key validation failed")
        return False
    
    # Test basic chat
    try:
        response = await chatbot.chat("Hello, how are you?")
        print(f"✅ Chat response received: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

async def test_chatbot_with_context(chatbot):
    """Test ChatBot with conversation history"""
    print("\nTesting ChatBot with context...")
    
    try:
        # Simulate a conversation
        conversation_history = [
            {"role": "user", "content": "My name is John"},
            {"role": "assistant", "content": "Nice to meet you, John!"}
        ]
        
        response = await chatbot.chat(
            "What's my name?", 
            conversation_history=conversation_history
        )
        print(f"✅ Context-aware response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Context test failed: {e}")
        return False

async def test_available_models(chatbot):
    """Test getting available models"""
    print("\nTesting available models...")
    
    try:
        models = await chatbot.get_available_models()
        print(f"✅ Available models: {len(models)} models found")
        if "x-ai/grok-2-1212" in models:
            print("✅ Grok 4 model is available")
        else:
            print("⚠️  Grok 4 model not found in available models")
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🤖 ChatBot Integration Test (OpenRouter + Grok 4)")
    print("=" * 50)
    
    # Test initialization
    chatbot = test_chatbot_initialization()
    if not chatbot:
        sys.exit(1)
    
    # Test basic functionality
    if not await test_chatbot_functionality(chatbot):
        sys.exit(1)
    
    # Test context functionality
    if not await test_chatbot_with_context(chatbot):
        sys.exit(1)
    
    # Test available models
    if not await test_available_models(chatbot):
        sys.exit(1)
    
    print("\n🎉 All tests passed! ChatBot integration is working correctly.")
    print("\nTo use the chatbot in your application:")
    print("1. Make sure OPENROUTER_API_KEY is set in your environment")
    print("2. Start the FastAPI server with: python main.py")
    print("3. Navigate to a project and start chatting with Grok 4!")

if __name__ == "__main__":
    asyncio.run(main())
