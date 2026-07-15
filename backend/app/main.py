from fastapi import FastAPI
from pydantic import BaseModel

from app.api.agent_routes import router as agent_router
from app.core.config import settings
from app.services.openai_service import ask_ai


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Hermes-style AI Agent for DevOps diagnostics and "
        "authorized bug-bounty assistance."
    ),
)

app.include_router(agent_router)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "agent_endpoint": "/agent/run",
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_ai(request.prompt)

    return {
        "response": answer,
    }
