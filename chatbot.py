import os
import httpx
import asyncio
from typing import List, Dict, Optional
from config import Config

class ChatBot:
    """
    A chatbot class that integrates with OpenRouter's API to provide conversational AI capabilities using Grok 4.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the ChatBot with OpenRouter API configuration.
        
        Args:
            api_key: OpenRouter API key. If not provided, will try to get from Config
            model: The model to use. If not provided, will use Config default (Grok 4)
        """
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.model = model or Config.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
        
        # Default system prompt
        self.default_system_prompt = "You are Grok, a helpful AI assistant with a witty and engaging personality. Provide clear, accurate, and helpful responses to user questions while maintaining your characteristic humor and directness."
    
    async def chat(self, message: str, system_prompt: Optional[str] = None, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Send a message to the chatbot and get a response.
        
        Args:
            message: The user's message
            system_prompt: Optional system prompt to override the default
            conversation_history: Optional list of previous messages in the conversation
            
        Returns:
            The chatbot's response as a string
        """
        try:
            # Prepare messages for the API call
            messages = []
            
            # Add system prompt
            system_msg = system_prompt or self.default_system_prompt
            messages.append({"role": "system", "content": system_msg})
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Make API call to OpenRouter
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/your-repo",  # Optional: for tracking
                        "X-Title": "Chatbot Platform"  # Optional: for tracking
                    },
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                    error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                    return f"OpenRouter API Error: {error_msg}"
            
        except httpx.TimeoutException:
            return "Request timeout. Please try again later."
        except httpx.ConnectError:
            return "Connection error. Please check your internet connection."
        except httpx.HTTPStatusError as e:
            return f"HTTP Error {e.response.status_code}: {e.response.text}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    async def chat_with_context(self, message: str, system_prompt: Optional[str] = None, project_messages: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Send a message with project-specific context from previous messages.
        
        Args:
            message: The user's message
            system_prompt: Optional system prompt for this project
            project_messages: List of previous messages from the project (from database)
            
        Returns:
            The chatbot's response as a string
        """
        # Convert project messages to OpenRouter format
        conversation_history = []
        if project_messages:
            # Take the last 10 messages to avoid token limits
            recent_messages = project_messages[-10:]
            for msg in recent_messages:
                conversation_history.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        return await self.chat(message, system_prompt, conversation_history)
    
    def set_model(self, model: str):
        """
        Change the OpenAI model being used.
        
        Args:
            model: The new model name (e.g., "gpt-4", "gpt-3.5-turbo")
        """
        self.model = model
    
    def get_available_models(self) -> List[str]:
        """
        Get a list of available OpenAI models.
        
        Returns:
            List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if "gpt" in model.id]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["gpt-3.5-turbo", "gpt-4"]  # Fallback to common models
    
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Make a simple API call to test the key
            self.client.models.list()
            return True
        except Exception:
            return False
