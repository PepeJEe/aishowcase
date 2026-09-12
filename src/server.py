from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config import settings
from src.logger import logger

from src.llm import receive_messages

app = FastAPI()


class ChatRequest(BaseModel):
    messages: list
    model: str = settings.default_model

#Basic fastapi post for ollama chat endpoint, with error handling for failed requests.
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        #response = await 
        response = await receive_messages(request.messages)
        return response
    except Exception as e:
            logger.error(f"Error during chat request: {e}")
            raise HTTPException(status_code=502, detail=str(e))
    
