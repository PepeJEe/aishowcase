from httpx import AsyncClient
from src.code.config import Settings
from src.code.logger import logger

async def receive_messages(messages):
    settings = Settings()
    try:
        full_messages = [{"role": "system", "content": settings.SYSTEM_PROMPT}] + messages
        async with AsyncClient(timeout=240) as client:
            response = await client.post(
                f"{settings.ollama_host}/api/chat",
                json={
                    "model": settings.model,
                    "messages": full_messages,
                    "stream": False,
                }
            )
            content = response.json()["message"]["content"]
            logger.info(f"Received response: {content[:50]}...")
            return response.json()["message"]["content"] #in message -> "full message" pick content

    except Exception as e:
        logger.error(f"Error while preparing messages: {e}")
        raise