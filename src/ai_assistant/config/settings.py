import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(
        os.getenv("PORT", "3000")
    )  # Changed to use env var with default
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")

    # Anthropic Settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # OpenRouter Settings
    OPEN_ROUTER_API_KEY: str = os.getenv("OPEN_ROUTER_API_KEY", "")

    # Tavily Settings
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Groq Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Serper Settings
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # Bot Settings
    BOT_NAME: str = os.getenv("BOT_NAME", "AI Assistant")

    # History Settings
    MESSAGE_HISTORY_LIMIT: int = int(os.getenv("MESSAGE_HISTORY_LIMIT", "5"))

    # Supabase Settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_USERS_TABLE: str = os.getenv("SUPABASE_USERS_TABLE", "users")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
