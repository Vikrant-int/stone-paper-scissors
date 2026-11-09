"""Core Stone Paper Scissors game rules.

This module is deliberately independent of any user interface. It contains no
``input()`` or ``print()`` calls, so the same rules can be reused by the current
terminal application and by a future desktop UI.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# Canonical choice names used throughout the backend.
STONE = "stone"
PAPER = "paper"
SCISSORS = "scissors"

Choice = str
Outcome = str

CHOICES: tuple[Choice, ...] = (STONE, PAPER, SCISSORS)

# Possible round outcomes.
PLAYER = "player"
COMPUTER = "computer"
DRAW = "draw"

# The original game accepted the single-letter shortcuts "ss", "p", and "s".
# Full names and common synonyms are accepted too, which keeps the backend
# convenient for future front ends without changing the original behaviour.
CHOICE_ALIASES: dict[str, Choice] = {
    "ss": STONE,
    "stone": STONE,
    "rock": STONE,
    "p": PAPER,
    "paper": PAPER,
    "s": SCISSORS,
    "scissor": SCISSORS,
    "scissors": SCISSORS,
}

# Each key beats the value:
# stone crushes scissors, scissors cut paper, and paper covers stone.
_WINNING_PAIRS: dict[Choice, Choice] = {
    STONE: SCISSORS,
    PAPER: STONE,
    SCISSORS: PAPER,
}


class InvalidChoiceError(ValueError):
    """Raised when a value cannot be mapped to a valid game choice."""

    def __init__(self, choice: object) -> None:
        self.choice = choice
        valid = ", ".join(CHOICES)
        super().__init__(f"invalid choice {choice!r}; choose one of: {valid}")


@dataclass(frozen=True)
class RoundResult:
    """The complete, UI-independent result of one round."""

    player_choice: Choice
    computer_choice: Choice
    winner: Outcome


def normalize_choice(choice: str) -> Choice:
    """Return the canonical choice name for a player-provided value.

    Matching is case-insensitive and ignores surrounding whitespace.

    Raises:
        InvalidChoiceError: If ``choice`` is not a recognised option.
    """

    if not isinstance(choice, str):
        raise InvalidChoiceError(choice)

    normalized = choice.strip().lower()
    try:
        return CHOICE_ALIASES[normalized]
    except KeyError as exc:
        raise InvalidChoiceError(choice) from exc


def get_computer_choice(rng: random.Random | None = None) -> Choice:
    """Return a random valid choice for the computer.

    Args:
        rng: Optional random source exposing ``choice(sequence)``. Injecting a
            seeded ``random.Random`` instance (or a test double) makes the
            selection deterministic for tests.
    """

    source = rng if rng is not None else random
    return source.choice(CHOICES)


def determine_winner(player_choice: str, computer_choice: str) -> Outcome:
    """Decide the winner of a round without performing any I/O.

    Both arguments accept the same aliases as :func:`normalize_choice`.

    Returns:
        ``PLAYER``, ``COMPUTER``, or ``DRAW``.

    Raises:
        InvalidChoiceError: If either choice is invalid.
    """

    player = normalize_choice(player_choice)
    computer = normalize_choice(computer_choice)

    if player == computer:
        return DRAW
    if _WINNING_PAIRS[player] == computer:
        return PLAYER
    return COMPUTER


def play_round(
    player_choice: str,
    rng: random.Random | None = None,
) -> RoundResult:
    """Play one round and return the player choice, computer choice, and winner.

    This function is pure apart from the optional random source, which makes it
    safe to call from a terminal, a test, or a future desktop UI.

    Raises:
        InvalidChoiceError: If ``player_choice`` is invalid.
    """

    player = normalize_choice(player_choice)
    computer = get_computer_choice(rng)
    return RoundResult(
        player_choice=player,
        computer_choice=computer,
        winner=determine_winner(player, computer),
    )
