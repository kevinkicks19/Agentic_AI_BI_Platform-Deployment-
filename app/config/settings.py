from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    # API Keys
    MEM0_API_KEY: str
    ARIZE_API_KEY: Optional[str] = None
    ARIZE_PROJECT_NAME: Optional[str] = None
    API_KEY: Optional[str] = None
    
    # Phoenix Arize Configuration
    PHOENIX_COLLECTOR_ENDPOINT: str = "https://app.phoenix.arize.com"
    PHOENIX_REST_API_BASE_URL: str = "https://app.phoenix.arize.com"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Business Intelligence Platform"
    
    # Model Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "llama2"
    MAX_CONVERSATION_TURNS: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields

# Create global settings instance
settings = Settings() 