"""Backend package for the Stone Paper Scissors game.

The package exposes reusable, UI-independent game rules. The terminal
application and any future desktop UI should import from here rather than
duplicating game logic.
"""

from backend.game_logic import (
    CHOICES,
    COMPUTER,
    DRAW,
    PAPER,
    PLAYER,
    SCISSORS,
    STONE,
    InvalidChoiceError,
    RoundResult,
    determine_winner,
    get_computer_choice,
    normalize_choice,
    play_round,
)

__all__ = [
    "CHOICES",
    "COMPUTER",
    "DRAW",
    "PAPER",
    "PLAYER",
    "SCISSORS",
    "STONE",
    "InvalidChoiceError",
    "RoundResult",
    "determine_winner",
    "get_computer_choice",
    "normalize_choice",
    "play_round",
]
