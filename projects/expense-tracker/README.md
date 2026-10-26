# Personal Expense Tracker

A small command-line app for recording everyday expenses. It is designed as a
Week 15 Python Journey capstone and uses only the Python standard library at
runtime.

## Setup

Use Python 3.12 or newer. From this directory, create and activate a virtual
environment if desired, then install pytest for the tests:

```bash
python -m pip install pytest
```

## Usage

Run the interactive menu from this directory:

```bash
python main.py
```

Choose an option to add transactions, list them, calculate totals, filter by
category, or save data. Saved records are written to `data/transactions.json`.
A missing data file is treated as an empty tracker and is created when saving.
Amounts must be positive numbers; descriptions and categories cannot be blank.

## Tests

Run the test suite from this directory:

```bash
python -m pytest -q
```

The tests cover validation, totals, case-insensitive category filtering, empty
records, JSON round-trips, missing files, and malformed or incomplete JSON.

## Main modules

- `main.py`: menu and terminal input/output.
- `src/core.py`: transaction validation, listing, filtering, and totals.
- `src/storage.py`: JSON persistence and validation when loading data.
- `tests/test_core.py`: automated behavior tests.

## Design decisions

Transactions are dictionaries with three named fields. A list keeps the records
in entry order, and JSON provides a simple human-readable file format. The
business rules are separate from terminal input so they can be tested without
interactive prompts. The app intentionally does not implement budgets, charts,
recurring payments, or multiple currencies.

## Example

```text
1. Them giao dich
Mo ta: Lunch
Danh muc: Food
So tien: 50
Da them giao dich.
3. Xem tong chi tieu
Tong chi tieu: 50.00
```

## Evidence and limitations

Run the test command above to reproduce the checks. The application is a local
single-user learning project; it does not encrypt the JSON file or synchronize
data between devices. The CLI uses simple text prompts and does not manage
income separately from expenses.

See [AI_USAGE.md](AI_USAGE.md) for a transparent record of AI assistance.
