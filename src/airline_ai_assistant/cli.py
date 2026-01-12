from __future__ import annotations

import argparse

from .config import load_settings
from .db import list_prices
from .seed import seed_default_prices
from .ui.gradio_app import launch


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Airline AI Assistant CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_ui = subparsers.add_parser("run-ui", help="Launch the Gradio UI")
    run_ui.add_argument("--host", default=None, help="Server host")
    run_ui.add_argument("--port", default=None, type=int, help="Server port")

    subparsers.add_parser("seed", help="Seed the database with default prices")
    subparsers.add_parser("list-prices", help="List ticket prices")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "run-ui":
        launch(host=args.host, port=args.port)
        return

    if args.command == "seed":
        seed_default_prices()
        return

    if args.command == "list-prices":
        settings = load_settings()
        for city, price in list_prices(settings.db_path):
            print(f"{city}: ${price}")
        return


if __name__ == "__main__":
    main()
