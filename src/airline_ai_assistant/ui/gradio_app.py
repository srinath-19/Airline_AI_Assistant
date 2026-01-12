from __future__ import annotations

import tempfile

import gradio as gr

from ..config import load_settings
from ..db import init_db
from ..llm import run_chat
from ..media import build_media_client, generate_image, generate_speech


def _ensure_db():
    settings = load_settings()
    init_db(settings.db_path)
    return settings


def _add_user_message(message: str, history: list[dict[str, str]] | None):
    history = history or []
    history.append({"role": "user", "content": message})
    return "", history


def _add_assistant_message(history: list[dict[str, str]]):
    if not history:
        return history
    settings = load_settings()
    user_message = history[-1]["content"]
    prior_history = history[:-1]
    assistant_message = run_chat(user_message, prior_history, settings, settings.db_path)
    history.append({"role": "assistant", "content": assistant_message})
    return history


def _generate_image(city: str):
    settings = load_settings()
    client = build_media_client(settings)
    return generate_image(client, city, settings.model_image)


def _generate_speech(text: str):
    settings = load_settings()
    client = build_media_client(settings)
    audio_bytes = generate_speech(client, text, settings.model_tts, settings.tts_voice)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        return tmp.name


def create_app() -> gr.Blocks:
    _ensure_db()
    with gr.Blocks() as app:
        gr.Markdown("# FlightAI Assistant")

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(height=520)
            message = gr.Textbox(label="Chat with our AI Assistant")
            message.submit(
                _add_user_message,
                inputs=[message, chatbot],
                outputs=[message, chatbot],
            ).then(_add_assistant_message, inputs=chatbot, outputs=chatbot)

        with gr.Tab("Image"):
            city = gr.Textbox(label="Destination city")
            image_button = gr.Button("Generate image")
            image_output = gr.Image(height=520, interactive=False)
            image_button.click(_generate_image, inputs=city, outputs=image_output)

        with gr.Tab("Speech"):
            text = gr.Textbox(label="Text to speak")
            speech_button = gr.Button("Generate speech")
            audio_output = gr.Audio(autoplay=True)
            speech_button.click(_generate_speech, inputs=text, outputs=audio_output)

    app.queue()
    return app


def launch(host: str | None = None, port: int | None = None):
    settings = load_settings()
    auth = None
    if settings.ui_auth_user and settings.ui_auth_pass:
        auth = (settings.ui_auth_user, settings.ui_auth_pass)
    app = create_app()
    app.launch(server_name=host, server_port=port, auth=auth)
