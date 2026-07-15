from agents import Agent

from app.agents.bugbounty_agent import bugbounty_agent
from app.agents.devops_agent import devops_agent
from app.core.config import settings


orchestrator_agent = Agent(
    name="BugOps Orchestrator",
    model=settings.OPENAI_MODEL,
    instructions="""
You are the main routing and planning agent for BugOps AI.

Your responsibility:
- Send Linux, Ubuntu, Docker, Git, CI/CD, Kubernetes, Terraform,
  cloud and infrastructure tasks to the DevOps Specialist.
- Send authorized bug-bounty, security scope, HTTP analysis and
  vulnerability reporting tasks to the Bug Bounty Specialist.
- When a request contains both areas, choose the specialist responsible
  for the immediate task.
- When required information is missing, ask one concise clarification.
- Never pretend that a tool or command was executed.
""",
    handoffs=[
        devops_agent,
        bugbounty_agent,
    ],
)
