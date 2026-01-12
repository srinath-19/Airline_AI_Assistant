from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import get_ticket_price


PRICE_FUNCTION = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False,
    },
}


def build_tools() -> list[dict[str, Any]]:
    return [{"type": "function", "function": PRICE_FUNCTION}]


def handle_tool_calls(message: Any, db_path: Path) -> list[dict[str, str]]:
    responses: list[dict[str, str]] = []
    for tool_call in message.tool_calls:
        if tool_call.function.name != "get_ticket_price":
            continue
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get("destination_city", "")
        price_details = get_ticket_price(db_path, city)
        responses.append(
            {
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id,
            }
        )
    return responses
