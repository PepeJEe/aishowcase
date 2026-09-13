from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.ai.narrator import narrator
from src.ai.parser import parse_event
from src.code.score import analyze_delay_event
from src.code.config import settings
from src.code.logger import logger
from src.code.delay import get_dep, nodes

from src.ai.llm import receive_messages

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

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

@app.get("/")
async def home():
     try:
          return FileResponse("src/static/interface.html")
     except Exception as e:
          logger.error(f"Error, can't load static files: {e}")

@app.post("/analyze", response_class=PlainTextResponse)
async def analyze(text: str = Form(...)): #parameter, what someone types in html input box
    try:
        node_ids = list(nodes.keys()) #gets all node ids, from node dictionary
        parsed = await parse_event(text, node_ids)
        print("PARSED:", parsed) 
        result = analyze_delay_event(nodes, get_dep(nodes), parsed["start_id"], parsed["delay_time"])
        report = await narrator(parsed, result)
        return report
    except Exception as e:
         logger.error(f"Report went wrong {e}")