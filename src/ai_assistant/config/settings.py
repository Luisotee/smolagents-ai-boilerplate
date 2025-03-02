import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")

    # Anthropic Settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Tavily Settings
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Groq Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Serper Settings
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # Bot Settings
    BOT_NAME: str = os.getenv("BOT_NAME", "AI Assistant")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
