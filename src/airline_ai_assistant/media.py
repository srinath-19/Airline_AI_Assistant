from __future__ import annotations

import base64
from io import BytesIO

from openai import OpenAI
from PIL import Image

from .config import Settings


def generate_image(client: OpenAI, city: str, model: str) -> Image.Image:
    image_response = client.images.generate(
        model=model,
        prompt=(
            "An image representing a vacation in "
            f"{city}, showing tourist spots and everything unique about {city}, "
            "in a vibrant pop-art style"
        ),
        size="1024x1024",
        n=1,
        response_format="b64_json",
    )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))


def generate_speech(client: OpenAI, text: str, model: str, voice: str) -> bytes:
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )
    return response.content


def build_media_client(settings: Settings) -> OpenAI:
    if settings.openai_api_key:
        return OpenAI(api_key=settings.openai_api_key)
    return OpenAI()
