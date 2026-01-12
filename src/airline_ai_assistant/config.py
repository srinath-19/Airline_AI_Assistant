from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


SYSTEM_MESSAGE = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so."
)


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    model_chat: str
    model_image: str
    model_tts: str
    tts_voice: str
    db_path: Path
    system_message: str
    ui_auth_user: str | None
    ui_auth_pass: str | None


def load_settings() -> Settings:
    load_dotenv(override=True)

    db_path = Path(os.getenv("AIRLINE_DB_PATH", "prices.db"))

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_chat=os.getenv("AIRLINE_CHAT_MODEL", "gpt-4.1-mini"),
        model_image=os.getenv("AIRLINE_IMAGE_MODEL", "dall-e-3"),
        model_tts=os.getenv("AIRLINE_TTS_MODEL", "gpt-4o-mini-tts"),
        tts_voice=os.getenv("AIRLINE_TTS_VOICE", "onyx"),
        db_path=db_path,
        system_message=os.getenv("AIRLINE_SYSTEM_MESSAGE", SYSTEM_MESSAGE),
        ui_auth_user=os.getenv("AIRLINE_UI_USER"),
        ui_auth_pass=os.getenv("AIRLINE_UI_PASS"),
    )
