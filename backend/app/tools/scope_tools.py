from __future__ import annotations

import re
from urllib.parse import urlparse

from agents import function_tool


def _extract_hostname(target: str) -> str:
    value = target.strip().lower()

    if "://" not in value:
        value = f"//{value}"

    parsed = urlparse(value)
    return (parsed.hostname or "").rstrip(".")


def _matches_scope(hostname: str, pattern: str) -> bool:
    normalized_pattern = pattern.strip().lower().rstrip(".")

    if not normalized_pattern:
        return False

    if normalized_pattern.startswith("*."):
        base_domain = normalized_pattern[2:]

        # Preliminary wildcard interpretation.
        return hostname.endswith(f".{base_domain}")

    return hostname == normalized_pattern


@function_tool
def check_bug_bounty_scope(
    target: str,
    allowed_scope: str,
) -> str:
    """
    Perform a preliminary target scope check.

    target:
        A hostname or URL such as api.example.com.

    allowed_scope:
        Comma or newline-separated scope entries, such as:
        example.com, *.example.com
    """
    hostname = _extract_hostname(target)

    if not hostname:
        return "Invalid target: hostname identify nahi ho saka."

    patterns = [
        value.strip()
        for value in re.split(r"[,\n]+", allowed_scope)
        if value.strip()
    ]

    if not patterns:
        return "Scope list empty hai. Program scope provide karo."

    matched_patterns = [
        pattern
        for pattern in patterns
        if _matches_scope(hostname, pattern)
    ]

    if matched_patterns:
        return (
            f"PRELIMINARY IN-SCOPE\n"
            f"Target: {hostname}\n"
            f"Matched entry: {matched_patterns[0]}\n\n"
            "Important: HackerOne/Bugcrowd program policy, exclusions, "
            "testing restrictions aur asset-specific rules manually verify karo."
        )

    return (
        f"NOT MATCHED\n"
        f"Target: {hostname}\n"
        f"Provided scope entries: {', '.join(patterns)}\n\n"
        "Is target par testing start mat karo jab tak program rules se "
        "written authorization confirm na ho."
    )
