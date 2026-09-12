from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_host: str = "https://ollama.pepevapp.com" #server
    default_model: str = "llama3.2:3b"
    max_tokens: int = 2048
    SYSTEM_PROMPT: str = "Your name is Testbot, you are a helpful assistant. You will answer questions and provide information to the best of your ability. If you do not know the answer, you will say I don't know."

    class Config:
        env_file = ".env"

settings = Settings()