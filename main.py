from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from httpx import AsyncClient
from config import settings


app = FastAPI()


class ChatRequest(BaseModel):
    messages: list
    model: str = settings.default_model

#Basic fastapi post for ollama chat endpoint, with error handling for failed requests.
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        async with AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{settings.ollama_host}/api/chat",
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "stream": False,
                }
            )
            response.raise_for_status() #error handling if occurs
            return response.json()
    except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
    
