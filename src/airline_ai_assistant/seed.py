from __future__ import annotations

from .config import load_settings
from .db import seed_prices


DEFAULT_PRICES = {
    "london": 799,
    "paris": 899,
    "tokyo": 1420,
    "sydney": 2999,
}


def seed_default_prices() -> None:
    settings = load_settings()
    seed_prices(settings.db_path, DEFAULT_PRICES)
