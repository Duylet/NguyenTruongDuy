"""JSON persistence for expense tracker transactions."""

import json
from pathlib import Path
from typing import Any

from src.core import Transaction, add_transaction


def save_transactions(path: Path, transactions: list[Transaction]) -> None:
    """Write transactions to a UTF-8 JSON file, creating parent folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(transactions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_transactions(path: Path) -> list[Transaction]:
    """Load and validate JSON data; a missing file means no saved records."""
    if not path.exists():
        return []
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}") from error

    if not isinstance(data, list):
        raise ValueError("transaction data must be a JSON list")

    transactions: list[Transaction] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("each transaction must be a JSON object")
        try:
            description = item["description"]
            category = item["category"]
            amount = item["amount"]
        except KeyError as error:
            raise ValueError(f"transaction is missing field: {error.args[0]}") from error
        if not isinstance(description, str) or not isinstance(category, str):
            raise ValueError("description and category must be text")
        add_transaction(transactions, description, category, amount)
    return transactions
