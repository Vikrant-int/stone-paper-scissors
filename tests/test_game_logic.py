"""Unit tests for :mod:`backend.game_logic`.

All randomness is injected or mocked, so every test is deterministic.
"""

from __future__ import annotations

import random
import unittest
from unittest.mock import patch

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


class FixedRandom:
    """Deterministic stand-in for ``random.Random``."""

    def __init__(self, value: str) -> None:
        self.value = value
        self.requested_sequences: list[tuple[str, ...]] = []

    def choice(self, sequence):
        self.requested_sequences.append(tuple(sequence))
        return self.value


class NormalizeChoiceTests(unittest.TestCase):
    def test_original_shortcuts_are_supported(self) -> None:
        self.assertEqual(normalize_choice("ss"), STONE)
        self.assertEqual(normalize_choice("p"), PAPER)
        self.assertEqual(normalize_choice("s"), SCISSORS)

    def test_full_names_are_supported(self) -> None:
        self.assertEqual(normalize_choice("stone"), STONE)
        self.assertEqual(normalize_choice("paper"), PAPER)
        self.assertEqual(normalize_choice("scissors"), SCISSORS)
        self.assertEqual(normalize_choice("scissor"), SCISSORS)
        self.assertEqual(normalize_choice("rock"), STONE)

    def test_matching_is_case_insensitive_and_trims_whitespace(self) -> None:
        self.assertEqual(normalize_choice("  SS  "), STONE)
        self.assertEqual(normalize_choice("Paper"), PAPER)
        self.assertEqual(normalize_choice("\tScissors\n"), SCISSORS)

    def test_invalid_choices_raise_a_clear_error(self) -> None:
        for invalid in ("", "x", "stone paper", "scissor paper", None, 1):
            with self.subTest(invalid=invalid):
                with self.assertRaises(InvalidChoiceError):
                    normalize_choice(invalid)


class DetermineWinnerTests(unittest.TestCase):
    # player choice, computer choice -> expected outcome
    EXPECTED_OUTCOMES = {
        (STONE, STONE): DRAW,
        (STONE, PAPER): COMPUTER,
        (STONE, SCISSORS): PLAYER,
        (PAPER, STONE): PLAYER,
        (PAPER, PAPER): DRAW,
        (PAPER, SCISSORS): COMPUTER,
        (SCISSORS, STONE): COMPUTER,
        (SCISSORS, PAPER): PLAYER,
        (SCISSORS, SCISSORS): DRAW,
    }

    def test_all_nine_outcomes(self) -> None:
        for (player, computer), expected in self.EXPECTED_OUTCOMES.items():
            with self.subTest(player=player, computer=computer):
                self.assertEqual(determine_winner(player, computer), expected)

    def test_every_choice_has_a_win_loss_and_draw_case(self) -> None:
        for choice in CHOICES:
            with self.subTest(choice=choice):
                outcomes = {
                    determine_winner(choice, computer)
                    for computer in CHOICES
                }
                self.assertEqual(outcomes, {PLAYER, COMPUTER, DRAW})

    def test_draw_conditions(self) -> None:
        for choice in CHOICES:
            with self.subTest(choice=choice):
                self.assertEqual(determine_winner(choice, choice), DRAW)

    def test_aliases_are_accepted(self) -> None:
        self.assertEqual(determine_winner("ss", "s"), PLAYER)
        self.assertEqual(determine_winner("p", "ss"), PLAYER)
        self.assertEqual(determine_winner("s", "p"), PLAYER)

    def test_invalid_player_choice_raises(self) -> None:
        with self.assertRaises(InvalidChoiceError):
            determine_winner("banana", STONE)

    def test_invalid_computer_choice_raises(self) -> None:
        with self.assertRaises(InvalidChoiceError):
            determine_winner(STONE, "banana")

    def test_non_string_choice_raises(self) -> None:
        with self.assertRaises(InvalidChoiceError):
            determine_winner(1, STONE)


class ComputerChoiceTests(unittest.TestCase):
    def test_computer_always_returns_a_valid_choice(self) -> None:
        rng = random.Random(2026)
        for _ in range(100):
            self.assertIn(get_computer_choice(rng), CHOICES)

    def test_computer_choice_uses_the_injected_random_source(self) -> None:
        rng = FixedRandom(SCISSORS)

        self.assertEqual(get_computer_choice(rng), SCISSORS)
        self.assertEqual(rng.requested_sequences, [CHOICES])

    def test_computer_choice_supports_controlled_values(self) -> None:
        for expected in CHOICES:
            with self.subTest(expected=expected):
                rng = FixedRandom(expected)
                self.assertEqual(get_computer_choice(rng), expected)

    def test_default_source_uses_the_random_module(self) -> None:
        with patch("backend.game_logic.random.choice", return_value=PAPER) as mocked:
            self.assertEqual(get_computer_choice(), PAPER)
            mocked.assert_called_once_with(CHOICES)

    def test_seeded_selection_is_reproducible(self) -> None:
        first = random.Random(1234)
        second = random.Random(1234)

        first_choices = [get_computer_choice(first) for _ in range(20)]
        second_choices = [get_computer_choice(second) for _ in range(20)]

        self.assertEqual(first_choices, second_choices)
        self.assertTrue(all(choice in CHOICES for choice in first_choices))


class PlayRoundTests(unittest.TestCase):
    def test_returns_a_complete_round_result(self) -> None:
        result = play_round(STONE, FixedRandom(SCISSORS))

        self.assertIsInstance(result, RoundResult)
        self.assertEqual(result.player_choice, STONE)
        self.assertEqual(result.computer_choice, SCISSORS)
        self.assertEqual(result.winner, PLAYER)

    def test_every_computer_choice_is_handled(self) -> None:
        for computer in CHOICES:
            with self.subTest(computer=computer):
                result = play_round(PAPER, FixedRandom(computer))
                self.assertEqual(result.player_choice, PAPER)
                self.assertEqual(result.computer_choice, computer)
                self.assertEqual(
                    result.winner,
                    determine_winner(PAPER, computer),
                )

    def test_player_aliases_are_normalised_in_the_result(self) -> None:
        result = play_round("  S  ", FixedRandom(PAPER))

        self.assertEqual(result.player_choice, SCISSORS)
        self.assertEqual(result.winner, PLAYER)

    def test_invalid_player_choice_raises_before_random_selection(self) -> None:
        rng = FixedRandom(STONE)

        with self.assertRaises(InvalidChoiceError):
            play_round("banana", rng)

        self.assertEqual(rng.requested_sequences, [])

    def test_result_is_immutable(self) -> None:
        result = play_round(STONE, FixedRandom(STONE))

        with self.assertRaises(AttributeError):
            result.winner = COMPUTER  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
