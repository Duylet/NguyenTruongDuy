"""Business rules for the personal expense tracker."""

from typing import TypedDict


class Transaction(TypedDict):
    description: str
    category: str
    amount: float


def add_transaction(
    transactions: list[Transaction],
    description: str,
    category: str,
    amount: float,
) -> Transaction:
    """Validate and append one transaction, returning the stored record."""
    clean_description = description.strip()
    clean_category = category.strip()
    if not clean_description:
        raise ValueError("description must not be empty")
    if not clean_category:
        raise ValueError("category must not be empty")
    if isinstance(amount, bool) or not isinstance(amount, int | float):
        raise ValueError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    transaction: Transaction = {
        "description": clean_description,
        "category": clean_category,
        "amount": float(amount),
    }
    transactions.append(transaction)
    return transaction


def list_transactions(transactions: list[Transaction]) -> list[Transaction]:
    """Return a shallow copy so callers cannot alter the original list."""
    return list(transactions)


def calculate_total(
    transactions: list[Transaction], category: str | None = None
) -> float:
    """Sum all amounts, optionally matching a category case-insensitively."""
    if category is None:
        selected = transactions
    else:
        selected = filter(
            lambda item: item["category"].casefold() == category.strip().casefold(),
            transactions,
        )
    return round(sum(item["amount"] for item in selected), 2)


def filter_by_category(
    transactions: list[Transaction], category: str
) -> list[Transaction]:
    """Return transactions in the requested category, ignoring case."""
    wanted = category.strip().casefold()
    return [item for item in transactions if item["category"].casefold() == wanted]
