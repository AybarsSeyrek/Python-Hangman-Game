# Python-Hangman-Game

This is an terminal-based Hangman game built with Python.
The game allows the player to choose a word category, select a difficulty level, guess letters, use hints, earn a score, and save game statistics using JSON file storage.
This project demonstrates core Python programming skills such as functions, dictionaries, lists, sets, JSON file handling, random word selection, input validation, string manipulation, statistics calculation, and modular project organization.

---

## Features

* Main menu system
* Player name input
* Multiple word categories
* Separate `words.json` file for the word bank
* Difficulty levels:

  * Easy
  * Medium
  * Hard
* Random word selection
* Better hyphen handling
* Guessed letters display
* Hint system
* Score system
* Game result summary
* JSON statistics saving
* Statistics screen
* Recent games display
* Word category viewer
* Rules screen
* Play again option
* Input validation
* Human-readable comments throughout the code

---

## Project Structure

```text
Python-Hangman-Game/
│
├── hangman_game.py
├── words.json
├── hangman_stats.json
└── README.md
```

### `hangman_game.py`

The main Python file that contains the game logic, including the menu, category selection, difficulty selection, guessing system, hints, scoring, statistics, and JSON saving.

### `words.json`

Stores the word categories and word lists used by the game.

Keeping the words in a separate JSON file makes the project more organized because the game logic and word data are separated.

### `hangman_stats.json`

Stores saved game results such as player name, category, difficulty, word, result, wrong guesses, hints used, score, and date/time.

This file is created automatically when the game saves results.

### `README.md`

Explains the project, features, file structure, how to run the game, and Python concepts demonstrated.

---

## How to Run

Make sure `hangman_game.py` and `words.json` are in the same folder.

Run the program with:

```bash
python hangman_game.py
```

or:

```bash
python3 hangman_game.py
```

---

## How the Game Works

1. The player starts the program.
2. The main menu is displayed.
3. The player chooses to play the game.
4. The player enters their name.
5. The player chooses a word category.
6. The player chooses a difficulty level.
7. The program randomly selects a word from `words.json`.
8. The player guesses one letter at a time.
9. Correct guesses reveal letters in the hidden word.
10. Wrong guesses add to the hangman drawing.
11. The player can use limited hints to reveal hidden letters.
12. The player wins if they reveal the full word.
13. The player loses if they reach the wrong guess limit.
14. The game calculates a score.
15. The result is saved to `hangman_stats.json`.

---

## Menu Options

When the program starts, the player sees this menu:

```text
1. Play Game
2. View Statistics
3. View Word Categories
4. View Rules
5. Exit
```

### 1. Play Game

Starts a new Hangman round.

The player enters their name, chooses a category, chooses a difficulty, and begins guessing letters.

### 2. View Statistics

Displays saved game statistics from `hangman_stats.json`.

The statistics screen shows:

* Total games played
* Wins
* Losses
* Win percentage
* Best score
* Average score
* Favorite category
* Recent games

### 3. View Word Categories

Shows all available word categories and how many words each category contains.

### 4. View Rules

Displays the rules of the Hangman game.

### 5. Exit

Closes the program.

---

## Difficulty Levels

The game includes three difficulty levels.

### Easy

* 8 wrong guesses allowed
* Shorter words
* 3 hints

### Medium

* 6 wrong guesses allowed
* Medium-length words
* 2 hints

### Hard

* 4 wrong guesses allowed
* Longer words allowed
* 1 hint

The difficulty affects the number of wrong guesses, number of hints, and possible word length.

---

## Word Categories

The words are stored in `words.json`.

Example categories include:

* Animals
* Countries
* Foods
* Sports
* Movies

Example JSON structure:

```json
{
    "Animals": [
        "tiger",
        "zebra",
        "elephant"
    ],
    "Foods": [
        "pizza",
        "burger",
        "pasta"
    ]
}
```

This makes it easy to add more categories or more words later without changing the Python code.

---

## Hyphen Handling

Some words contain hyphens, such as:

```text
polar-bear
red-panda
star-wars
```

The game automatically reveals hyphens instead of hiding them as underscores.

Example:

```text
_ _ _ _ _ - _ _ _ _
```

This makes the hidden word easier to read and improves the game experience.

---

## Hint System

The player has a limited number of hints depending on the difficulty.

A hint reveals one random hidden letter in the word.

Using hints reduces the final score.

This adds strategy because the player must decide whether the hint is worth the score penalty.

---

## Score System

The game calculates a score at the end of each round.

The score is based on:

* Difficulty level
* Number of wrong guesses
* Number of hints used
* Whether the player won or lost

Example scoring idea:

```python
score = base_score - wrong_guesses * 10 - hints_used * 15
```

If the player loses, the score becomes `0`.

---

## Statistics Saving

Each finished game is saved to `hangman_stats.json`.

Example saved result:

```json
{
    "player_name": "Aybars",
    "category": "Animals",
    "difficulty": "Medium",
    "word": "elephant",
    "result": "Won",
    "wrong_guesses": 2,
    "hints_used": 1,
    "score": 115,
    "date_time": "2026-06-06 14:30:00"
}
```

This demonstrates persistent data storage because the game can remember results after the program closes.

---

## Technical Concepts Demonstrated

### Functions and Modular Code

The program is separated into functions such as:

```python
display_main_menu()
choose_category()
choose_difficulty()
play_game()
calculate_score()
save_game_result()
view_statistics()
```

This makes the code easier to read, test, and expand.

---

### Lists

Lists are used to store words, hidden letters, hangman art, and game history.

Example:

```python
hint = ["_"] * len(answer)
```

---

### Dictionaries

Dictionaries are used for difficulty settings and word categories.

Example:

```python
DIFFICULTIES = {
    "Easy": {
        "max_wrong_guesses": 8,
        "max_word_length": 6,
        "hints": 3
    }
}
```

---

### Sets

A set is used to track guessed letters.

```python
guessed_letters = set()
```

Sets are useful because they prevent duplicate guessed letters.

---

### JSON File Handling

The program reads word data from `words.json` and saves statistics to `hangman_stats.json`.

```python
json.load(file)
json.dump(stats, file, indent=4)
```

This demonstrates how Python can work with external data files.

---

### Random Word Selection

The program uses the `random` module to choose a random word.

```python
random.choice(possible_words)
```

It also uses random selection for hints.

---

### Input Validation

The game checks user input to make sure the player enters valid menu choices, valid category choices, valid difficulty choices, and single-letter guesses.

This prevents the program from crashing because of bad input.

---

### String Handling

The game works with strings to check letters, reveal correct guesses, handle hyphens, and display the hidden word.

Example:

```python
if answer[index] == guess:
    hint[index] = guess
```

---

### List Comprehension

The game filters words based on difficulty.

```python
filtered_words = [
    word for word in words
    if len(word.replace("-", "")) <= max_length
]
```

This demonstrates a clean way to create a filtered list.

---

### Statistics Calculation

The program calculates:

* Total games
* Wins
* Losses
* Win percentage
* Best score
* Average score
* Favorite category

This demonstrates loops, calculations, and working with saved JSON data.

---

## Python Concepts Practiced

This project practices the following Python concepts:

* Variables
* Constants
* Functions
* Lists
* Dictionaries
* Sets
* Loops
* Conditional statements
* User input
* Input validation
* String manipulation
* Random selection
* JSON file handling
* File reading
* File writing
* Error handling
* Date and time
* List comprehensions
* Statistics calculations
* Modular program structure

---

## Standard Libraries Used

This project only uses Python standard libraries.

```python
import random
import json
import os
from datetime import datetime
```

### `random`

Used to randomly choose words and reveal random hint letters.

### `json`

Used to load word categories and save game statistics.

### `os`

Used to check whether the statistics file exists.

### `datetime`

Used to add a date and time to each saved game result.

---

## What I Learned

While building this project, I practiced turning a simple Hangman game into a more complete Python terminal application.

I learned how to separate word data from game logic using a JSON file, create a menu-based program, use dictionaries for difficulty settings, use sets to track guessed letters, validate user input, calculate scores, and save game statistics.

This project also helped me understand how to organize a larger Python program using multiple functions and external data files.
