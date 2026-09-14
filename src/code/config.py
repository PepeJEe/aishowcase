from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_host: str = "https://ollama.pepevapp.com" #server
    default_model: str = "qwen2.5:1.5b"
    max_tokens: int = 2048
    SYSTEM_PROMPT: str = "You are computer supply chain risk and escalation alarm. You output the necessary details and info based on what you will receive from the user."

    class Config:
        env_file = ".env"

settings = Settings()