"""Exercise 01: class, object and methods."""


class Progress:
    """Track completed work out of a total."""

    def __init__(self, completed: int, total: int) -> None:
        if total < 1:
            raise ValueError("total must be positive")
        if not 0 <= completed <= total:
            raise ValueError("completed must be between 0 and total")
        self.completed = completed
        self.total = total

    def percentage(self) -> float:
        """Return the completed percentage."""
        return self.completed / self.total * 100

    def __str__(self) -> str:
        """Return a short, readable progress summary."""
        return f"Progress: {self.completed}/{self.total} ({self.percentage():.0f}%)"


if __name__ == "__main__":
    progress = Progress(completed=3, total=4)
    print(progress)
