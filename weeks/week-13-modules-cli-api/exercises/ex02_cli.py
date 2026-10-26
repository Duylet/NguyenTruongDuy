"""Exercise 02: add one argparse option to a small CLI."""

import argparse


def parser() -> argparse.ArgumentParser:
    """Build a parser that requires an integer turn count."""
    result = argparse.ArgumentParser(description="Show a requested turn count")
    result.add_argument("--turn", type=int, required=True, help="number of turns")
    return result


def main() -> None:
    """Parse learner arguments and display the resulting namespace."""
    print(parser().parse_args())


if __name__ == "__main__":
    main()
