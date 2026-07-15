from __future__ import annotations

from typing import Literal

from agents import Runner

from app.agents.bugbounty_agent import bugbounty_agent
from app.agents.devops_agent import devops_agent
from app.agents.orchestrator import orchestrator_agent


AgentMode = Literal["auto", "devops", "bugbounty"]


AGENTS = {
    "auto": orchestrator_agent,
    "devops": devops_agent,
    "bugbounty": bugbounty_agent,
}


async def execute_agent(
    prompt: str,
    mode: AgentMode = "auto",
) -> dict[str, str]:
    starting_agent = AGENTS[mode]

    result = await Runner.run(
        starting_agent,
        prompt,
        max_turns=8,
    )

    return {
        "mode": mode,
        "agent": result.last_agent.name,
        "answer": str(result.final_output),
    }
