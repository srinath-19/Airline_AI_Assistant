from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Iterable


def init_db(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)"
        )
        conn.commit()


def set_ticket_price(db_path: Path, city: str, price: float) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (city, price) VALUES (?, ?) "
            "ON CONFLICT(city) DO UPDATE SET price = ?",
            (city.lower(), price, price),
        )
        conn.commit()


def get_ticket_price(db_path: Path, city: str) -> str:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM prices WHERE city = ?", (city.lower(),))
        result = cursor.fetchone()
        if result:
            return f"Ticket price to {city} is ${result[0]}"
        return "No price data available for this city"


def seed_prices(db_path: Path, prices: dict[str, float]) -> None:
    init_db(db_path)
    for city, price in prices.items():
        set_ticket_price(db_path, city, price)


def list_prices(db_path: Path) -> Iterable[tuple[str, float]]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT city, price FROM prices ORDER BY city")
        return cursor.fetchall()
