from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings
from app.services.openai_service import ask_ai

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_ai(request.prompt)

    return {
        "response": answer
    }    

