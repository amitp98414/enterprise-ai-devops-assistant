from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal

from agents import function_tool


CheckName = Literal[
    "os",
    "uptime",
    "disk",
    "memory",
    "git_status",
    "docker_ps",
    "compose_ps",
]


COMMANDS: dict[str, list[str]] = {
    "os": ["uname", "-a"],
    "uptime": ["uptime"],
    "disk": ["df", "-h"],
    "memory": ["free", "-m"],
    "git_status": ["git", "status", "--short", "--branch"],
    "docker_ps": [
        "docker",
        "ps",
        "--format",
        "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}",
    ],
    "compose_ps": ["docker", "compose", "ps"],
}


def _find_project_directory() -> Path:
    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        if (parent / ".git").exists():
            return parent

    return Path.cwd()


@function_tool
def ubuntu_readonly_check(check: CheckName) -> str:
    """
    Run one approved read-only Ubuntu or DevOps diagnostic check.

    Available checks:
    os, uptime, disk, memory, git_status, docker_ps and compose_ps.
    This tool cannot accept or execute arbitrary shell commands.
    """
    command = COMMANDS[check]

    try:
        result = subprocess.run(
            command,
            cwd=_find_project_directory(),
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
            shell=False,
        )
    except FileNotFoundError:
        return (
            f"Tool unavailable: '{command[0]}' command installed nahi hai "
            "ya PATH me available nahi hai."
        )
    except subprocess.TimeoutExpired:
        return "Command 20 seconds ke timeout ke baad stop kar diya gaya."
    except Exception as exc:
        return f"Safe diagnostic tool error: {type(exc).__name__}"

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    output_parts = [
        f"$ {' '.join(command)}",
        f"exit_code={result.returncode}",
    ]

    if stdout:
        output_parts.append(stdout)

    if stderr:
        output_parts.append(f"stderr:\n{stderr}")

    if not stdout and not stderr:
        output_parts.append("(no output)")

    return "\n".join(output_parts)[:12000]
