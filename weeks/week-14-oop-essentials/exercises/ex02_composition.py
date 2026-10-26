"""Exercise 02: compose Bot with a replaceable strategy."""

from collections.abc import Callable

State = dict[str, int]
Strategy = Callable[[State], str]


class Bot:
    """Delegate action selection to a strategy function."""

    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def choose_action(self, state: State) -> str:
        """Choose an action using the currently configured strategy."""
        return self.strategy(state)


def move_toward_goal(state: State) -> str:
    """Move one step toward goal 0 or 4, or wait when already there."""
    position = state["position"]
    goal = state["goal"]
    if position < goal:
        return "right"
    if position > goal:
        return "left"
    return "wait"


def defensive(state: State) -> str:
    """Wait when the opponent is close; otherwise move toward the goal."""
    opponent = state.get("opponent_position")
    if opponent is not None and abs(opponent - state["position"]) <= 1:
        return "wait"
    return move_toward_goal(state)


def balanced(state: State) -> str:
    """Use straightforward movement toward the goal."""
    return move_toward_goal(state)


def aggressive(state: State) -> str:
    """Use straightforward movement toward the goal."""
    return move_toward_goal(state)


if __name__ == "__main__":
    state = {"position": 1, "opponent_position": 4, "goal": 4}
    bot = Bot(balanced)
    print(bot.choose_action(state))
    bot.strategy = defensive
    print(bot.choose_action(state))
