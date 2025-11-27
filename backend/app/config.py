import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()

def parse_int_env(var_name: str, default: int) -> int:
    value = os.getenv(var_name, str(default))
    # Remove comments and strip whitespace
    value = value.split('#')[0].strip()
    return int(value)

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./aichatbot.db")

    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    huggingface_api_token: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
    whisper_api_key: str = os.getenv("HUGGINGFACE_API_TOKEN", "")

    # API Endpoints
    huggingface_whisper_endpoint: str = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

    # Model Configuration
    gemini_model_name: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-preview-04-17")

    # File Upload Settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/ai-math-chatbot-uploads")
    max_file_size: int = parse_int_env("MAX_FILE_SIZE", 20 * 1024 * 1024)  # 20MB default

    # Audio Upload Settings
    audio_dir: str = os.getenv("AUDIO_DIR", "/tmp/ai-math-chatbot-audio")
    max_audio_size: int = parse_int_env("MAX_AUDIO_SIZE", 10 * 1024 * 1024)  # 10MB default

    # Server Settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    # In Pydantic v2, Config is replaced with model_config
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Allow extra fields in environment variables
    }

@lru_cache()
def get_settings():
    return Settings()

# Get API Keys from environment variables for backward compatibility
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Define the Hugging Face Inference API endpoint for Whisper
HUGGINGFACE_WHISPER_ENDPOINT = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

# Basic validation
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY environment variable not set.")
if not HUGGINGFACE_API_TOKEN:
    print("Warning: HUGGINGFACE_API_TOKEN environment variable not set. Whisper functionality will be disabled.")