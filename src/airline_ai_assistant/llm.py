from __future__ import annotations

from pathlib import Path
from typing import Any

from openai import OpenAI

from .config import Settings
from .tools import build_tools, handle_tool_calls


def build_client(settings: Settings) -> OpenAI:
    if settings.openai_api_key:
        return OpenAI(api_key=settings.openai_api_key)
    return OpenAI()


def run_chat(
    message: str,
    history: list[dict[str, str]],
    settings: Settings,
    db_path: Path,
) -> str:
    messages: list[dict[str, str]] = [{"role": "system", "content": settings.system_message}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    client = build_client(settings)
    tools = build_tools()
    response = client.chat.completions.create(
        model=settings.model_chat,
        messages=messages,
        tools=tools,
    )

    while response.choices[0].finish_reason == "tool_calls":
        tool_message = response.choices[0].message
        tool_responses = handle_tool_calls(tool_message, db_path)
        messages.append(tool_message)
        messages.extend(tool_responses)
        response = client.chat.completions.create(
            model=settings.model_chat,
            messages=messages,
            tools=tools,
        )

    return response.choices[0].message.content or ""
