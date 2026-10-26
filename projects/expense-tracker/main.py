"""Command-line interface for the personal expense tracker."""

from pathlib import Path

from src.core import (
    Transaction,
    add_transaction,
    calculate_total,
    filter_by_category,
    list_transactions,
)
from src.storage import load_transactions, save_transactions

DATA_FILE = Path(__file__).parent / "data" / "transactions.json"


def show_transactions(transactions: list[Transaction]) -> None:
    """Print each transaction and the total amount."""
    if not transactions:
        print("Chua co giao dich.")
        return
    for index, item in enumerate(transactions, start=1):
        print(
            f"{index}. {item['description']} | {item['category']} "
            f"| {item['amount']:.2f}"
        )
    print(f"Tong: {calculate_total(transactions):.2f}")


def prompt_for_transaction(transactions: list[Transaction]) -> None:
    """Read and validate one transaction from the terminal."""
    description = input("Mo ta: ")
    category = input("Danh muc: ")
    amount_text = input("So tien: ").strip()
    try:
        amount = float(amount_text)
        add_transaction(transactions, description, category, amount)
    except ValueError as error:
        print(f"Khong them duoc giao dich: {error}")
    else:
        print("Da them giao dich.")


def run() -> None:
    """Run the menu until the user chooses to exit."""
    try:
        transactions = load_transactions(DATA_FILE)
    except (OSError, ValueError) as error:
        print(f"Khong doc duoc du lieu: {error}")
        transactions = []

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Them giao dich")
        print("2. Xem giao dich")
        print("3. Xem tong chi tieu")
        print("4. Loc theo danh muc")
        print("5. Luu du lieu")
        print("0. Thoat")
        choice = input("Chon: ").strip()

        if choice == "1":
            prompt_for_transaction(transactions)
        elif choice == "2":
            show_transactions(list_transactions(transactions))
        elif choice == "3":
            print(f"Tong chi tieu: {calculate_total(transactions):.2f}")
        elif choice == "4":
            category = input("Danh muc can loc: ")
            show_transactions(filter_by_category(transactions, category))
        elif choice == "5":
            try:
                save_transactions(DATA_FILE, transactions)
            except OSError as error:
                print(f"Khong luu duoc du lieu: {error}")
            else:
                print("Da luu du lieu.")
        elif choice == "0":
            print("Tam biet!")
            return
        else:
            print("Lua chon khong hop le. Hay chon lai.")


if __name__ == "__main__":
    run()
