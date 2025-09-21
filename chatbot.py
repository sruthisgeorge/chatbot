import os
import openai
from typing import List, Dict, Optional
from config import Config

class ChatBot:
    """
    A chatbot class that integrates with OpenAI's API to provide conversational AI capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the ChatBot with OpenAI API configuration.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from Config
            model: The OpenAI model to use. If not provided, will use Config default
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Default system prompt
        self.default_system_prompt = "You are a helpful AI assistant. Provide clear, accurate, and helpful responses to user questions."
    
    def chat(self, message: str, system_prompt: Optional[str] = None, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
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
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract and return the response
            return response.choices[0].message.content.strip()
            
        except openai.APIError as e:
            return f"OpenAI API Error: {str(e)}"
        except openai.RateLimitError as e:
            return f"Rate limit exceeded. Please try again later. Error: {str(e)}"
        except openai.APIConnectionError as e:
            return f"Connection error. Please check your internet connection. Error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    def chat_with_context(self, message: str, system_prompt: Optional[str] = None, project_messages: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Send a message with project-specific context from previous messages.
        
        Args:
            message: The user's message
            system_prompt: Optional system prompt for this project
            project_messages: List of previous messages from the project (from database)
            
        Returns:
            The chatbot's response as a string
        """
        # Convert project messages to OpenAI format
        conversation_history = []
        if project_messages:
            # Take the last 10 messages to avoid token limits
            recent_messages = project_messages[-10:]
            for msg in recent_messages:
                conversation_history.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        return self.chat(message, system_prompt, conversation_history)
    
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
