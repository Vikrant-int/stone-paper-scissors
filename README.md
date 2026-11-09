# Stone Paper Scissors

A clean, beginner-friendly Stone Paper Scissors game written in Python. The
project keeps the original terminal gameplay while separating the game rules
from the interface, so a desktop UI can be added later without rewriting the
rules.

## Features

- Single-round terminal game with the original `ss` / `p` / `s` shortcuts.
- Clear instructions and friendly handling of invalid input.
- UI-independent backend that can be reused by any front end.
- Random computer selection with an injectable random source for deterministic
  testing.
- Comprehensive unit tests using Python's built-in `unittest` framework.
- No third-party dependencies.

## Technologies Used

- Python 3.10+
- Python standard library (`random`, `dataclasses`, `unittest`)

## Project Structure

```text
stone-paper-scissors/
│
├── backend/
│   ├── __init__.py
│   └── game_logic.py      # Reusable rules, choices, and round results
│
├── frontend/
│   └── __init__.py        # Placeholder for a future desktop UI
│
├── tests/
│   ├── __init__.py
│   └── test_game_logic.py # Automated backend tests
│
├── main.py                # Terminal application
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Vikrant-int/stone-paper-scissors.git
   cd stone-paper-scissors
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The project uses only the Python standard library, so there are no
   third-party packages to install.

## How to Run the Game

From the project root:

```bash
python main.py
```

Enter one of the following choices:

| Input | Choice   |
|-------|----------|
| `ss`  | Stone    |
| `p`   | Paper    |
| `s`   | Scissor  |
| `q`   | Quit     |

Invalid input is rejected with a short message, and you are prompted again.

## How to Run Tests

From the project root:

```bash
python -m unittest discover -v
```

You can also run the test module directly:

```bash
python -m unittest tests.test_game_logic -v
```

## Example Gameplay

```text
========================================
      STONE - PAPER - SCISSORS
========================================
Choose one:
  ss -> stone
  p  -> paper
  s  -> scissor
  q  -> quit

enter your choice: ss
your choice is stone
computer choice is scissor
YOU WIN !!!!
```

## Backend Architecture

`backend/game_logic.py` contains all game rules and performs no terminal input
or output:

- `CHOICES` defines the three valid choices.
- `normalize_choice()` validates input and maps aliases such as `ss` to a
  canonical choice.
- `get_computer_choice()` selects a random valid choice. It accepts an optional
  random source so tests can control the result.
- `determine_winner()` returns `player`, `computer`, or `draw`.
- `play_round()` combines the above and returns a frozen `RoundResult`
  containing the player choice, computer choice, and winner.

`main.py` is the only module responsible for `input()` and `print()`. The
backend has no dependency on the frontend or on the terminal interface.

## Future Development Plans

- Add a desktop UI in `frontend/` (for example with Tkinter, PySide, or
  CustomTkinter) that calls `backend.game_logic.play_round()` directly.
- Keep score history and display it in the UI.
- Add configurable multi-round matches.
- Add a settings screen for sound, themes, and difficulty.
- Package the desktop application as a standalone executable.

Because the rules are already isolated in the backend, none of these features
require changing how Stone Paper Scissors is played.
