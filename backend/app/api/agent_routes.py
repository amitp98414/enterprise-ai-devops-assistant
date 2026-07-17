from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.security import enforce_rate_limit
from app.services.agent_service import execute_agent


router = APIRouter(
    prefix="/agent",
    tags=["OpsSage AI Agent"],
)


class AgentRunRequest(BaseModel):
    prompt: str = Field(
        min_length=3,
        max_length=12000,
    )
    mode: Literal["auto", "devops", "bugbounty"] = "auto"


@router.get("/modes")
def list_agent_modes():
    return {
        "modes": {
            "auto": "Orchestrator automatically selects a specialist",
            "devops": "Ubuntu, Docker, Git and infrastructure specialist",
            "bugbounty": "Authorized bug-bounty analysis specialist",
        }
    }


@router.post("/run")
async def run_agent(
    request: AgentRunRequest,
    _: str = Depends(enforce_rate_limit),
):
    try:
        return await execute_agent(
            prompt=request.prompt,
            mode=request.mode,
        )
    except Exception as exc:
        print(f"Agent execution failed: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=500,
            detail=(
                "The agent could not execute. Check the backend terminal logs. "
                "Verify the API key, model name, and internet connection. "
            ),
        ) from exc
