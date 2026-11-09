"""Terminal entry point for the Stone Paper Scissors game.

All game rules live in ``backend.game_logic``. This module is responsible only
for terminal input, output, and formatting.
"""

from __future__ import annotations

from backend.game_logic import (
    COMPUTER,
    DRAW,
    PAPER,
    PLAYER,
    SCISSORS,
    STONE,
    InvalidChoiceError,
    normalize_choice,
    play_round,
)

# Human-readable labels. The original game displayed "scissor" (singular).
DISPLAY_NAMES = {
    STONE: "stone",
    PAPER: "paper",
    SCISSORS: "scissor",
}

_QUIT_COMMANDS = {"q", "quit", "exit"}


def print_instructions() -> None:
    """Display the game instructions and accepted input shortcuts."""

    print("=" * 40)
    print("      STONE - PAPER - SCISSORS")
    print("=" * 40)
    print("Choose one:")
    print("  ss -> stone")
    print("  p  -> paper")
    print("  s  -> scissor")
    print("  q  -> quit")
    print()


def prompt_player_choice() -> str | None:
    """Prompt until a valid choice is entered, or return ``None`` to quit."""

    while True:
        try:
            raw_choice = input("enter your choice: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return None

        if raw_choice.strip().lower() in _QUIT_COMMANDS:
            print("Goodbye!")
            return None

        try:
            return normalize_choice(raw_choice)
        except InvalidChoiceError:
            print("Invalid choice. Please enter ss, p, or s (or q to quit).")


def main() -> int:
    """Run one round of the terminal game."""

    print_instructions()

    player_choice = prompt_player_choice()
    if player_choice is None:
        return 0

    result = play_round(player_choice)

    print(
        f"your choice is {DISPLAY_NAMES[result.player_choice]} "
        f"\ncomputer choice is {DISPLAY_NAMES[result.computer_choice]}"
    )

    if result.winner == DRAW:
        print("GAME DRAW !!!!")
    elif result.winner == PLAYER:
        print("YOU WIN !!!!")
    elif result.winner == COMPUTER:
        print("COMPUTER WIN !!!!")
    else:  # Defensive: backend outcomes are limited to the three above.
        raise RuntimeError(f"Unexpected round outcome: {result.winner!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
