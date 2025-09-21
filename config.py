import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Chatbot Platform"""
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-2-1212")  # Grok 4 model
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
    
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # File Upload Configuration
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
    
    @classmethod
    def validate_openrouter_config(cls):
        """Validate OpenRouter configuration"""
        if not cls.OPENROUTER_API_KEY:
            return False, "OPENROUTER_API_KEY environment variable is not set"
        return True, "OpenRouter configuration is valid"
    
    @classmethod
    def get_openrouter_config(cls):
        """Get OpenRouter configuration as a dictionary"""
        return {
            "api_key": cls.OPENROUTER_API_KEY,
            "model": cls.OPENROUTER_MODEL
        }
