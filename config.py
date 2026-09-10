from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_host: str = "192.168.0.200:11434"
    default_model: str = "llama3.2:3b"
    max_tokens: int = 2048

    class Config:
        env_file = ".env"

settings = Settings()