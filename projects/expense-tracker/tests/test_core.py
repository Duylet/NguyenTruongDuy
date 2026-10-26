"""Tests for the expense tracker business rules and storage."""

import json

import pytest

from src.core import (
    add_transaction,
    calculate_total,
    filter_by_category,
    list_transactions,
)
from src.storage import load_transactions, save_transactions


def sample_transactions() -> list[dict[str, str | float]]:
    return [
        {"description": "Lunch", "category": "Food", "amount": 50.0},
        {"description": "Bus", "category": "Transport", "amount": 12.5},
    ]


def test_add_transaction_trims_text_and_stores_amount_as_float() -> None:
    records: list[dict[str, str | float]] = []
    added = add_transaction(records, " Lunch ", " Food ", 50)
    assert added == {"description": "Lunch", "category": "Food", "amount": 50.0}
    assert records == [added]


def test_add_transaction_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="description"):
        add_transaction([], "  ", "Food", 10)


def test_add_transaction_rejects_empty_category() -> None:
    with pytest.raises(ValueError, match="category"):
        add_transaction([], "Lunch", " ", 10)


def test_add_transaction_rejects_non_positive_amount() -> None:
    for amount in (0, -2):
        with pytest.raises(ValueError, match="greater than zero"):
            add_transaction([], "Lunch", "Food", amount)


def test_calculate_total_and_category_filter() -> None:
    records = sample_transactions()
    assert calculate_total(records) == 62.5
    assert calculate_total(records, "food") == 50.0
    assert filter_by_category(records, "TRANSPORT") == [records[1]]


def test_empty_total_is_zero() -> None:
    assert calculate_total([]) == 0


def test_list_transactions_returns_separate_list() -> None:
    records = sample_transactions()
    copied = list_transactions(records)
    copied.clear()
    assert len(records) == 2


def test_save_and_load_round_trip(tmp_path) -> None:
    records = sample_transactions()
    destination = tmp_path / "nested" / "transactions.json"
    save_transactions(destination, records)
    assert load_transactions(destination) == records


def test_load_missing_file_returns_empty_list(tmp_path) -> None:
    assert load_transactions(tmp_path / "missing.json") == []


def test_load_invalid_json_raises_value_error(tmp_path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        load_transactions(path)


def test_load_rejects_missing_transaction_field(tmp_path) -> None:
    path = tmp_path / "missing-field.json"
    path.write_text(json.dumps([{"description": "Tea", "amount": 5}]), encoding="utf-8")
    with pytest.raises(ValueError, match="missing field"):
        load_transactions(path)
