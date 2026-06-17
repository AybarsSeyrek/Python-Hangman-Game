import random
import json
import os
from datetime import datetime


WORDS_FILE = "words.json"
STATS_FILE = "hangman_stats.json"


DIFFICULTIES = {
    "Easy": {
        "max_wrong_guesses": 8,
        "max_word_length": 6,
        "hints": 3
    },
    "Medium": {
        "max_wrong_guesses": 6,
        "max_word_length": 10,
        "hints": 2
    },
    "Hard": {
        "max_wrong_guesses": 4,
        "max_word_length": 100,
        "hints": 1
    }
}


def get_hangman_art(max_wrong_guesses):
    full_art = [
        ("   ", "   ", "   "),
        (" o ", "   ", "   "),
        (" o ", " | ", "   "),
        (" o ", "/| ", "   "),
        (" o ", "/|\\", "   "),
        (" o ", "/|\\", "/  "),
        (" o ", "/|\\", "/ \\"),
        (" o ", "/|\\", "/ \\", "Game is almost over..."),
        (" o ", "/|\\", "/ \\", "Last chance!")
    ]

    return full_art[:max_wrong_guesses + 1]


def load_word_categories():
    # This program now requires words.json to exist.
    # This keeps the word data separate from the game logic.
    if not os.path.exists(WORDS_FILE):
        print(f"\nError: {WORDS_FILE} was not found.")
        print("Please create words.json in the same folder as hangman_game.py.")
        return None

    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as file:
            word_categories = json.load(file)

        if not word_categories:
            print("\nError: words.json is empty.")
            return None

        return word_categories

    except json.JSONDecodeError:
        print("\nError: words.json is not valid JSON.")
        return None


def load_stats():
    if not os.path.exists(STATS_FILE):
        return []

    try:
        with open(STATS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_main_menu():
    print("=" * 50)
    print("              ADVANCED HANGMAN")
    print("=" * 50)
    print("1. Play Game")
    print("2. View Statistics")
    print("3. View Word Categories")
    print("4. View Rules")
    print("5. Exit")
    print("=" * 50)


def get_menu_choice(valid_choices):
    while True:
        choice = input("Enter your choice: ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please try again.")


def get_player_name():
    while True:
        name = input("Enter your name: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def choose_category(word_categories):
    categories = list(word_categories.keys())

    print("\nChoose a category:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Enter category number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

        print("Invalid category. Please choose a valid number.")


def choose_difficulty():
    difficulties = list(DIFFICULTIES.keys())

    print("\nChoose difficulty:")
    for index, difficulty in enumerate(difficulties, start=1):
        settings = DIFFICULTIES[difficulty]
        print(
            f"{index}. {difficulty} "
            f"- {settings['max_wrong_guesses']} wrong guesses, "
            f"{settings['hints']} hint(s)"
        )

    while True:
        choice = input("Enter difficulty number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(difficulties):
                return difficulties[choice - 1]

        print("Invalid difficulty. Please choose a valid number.")


def filter_words_by_difficulty(words, difficulty):
    max_length = DIFFICULTIES[difficulty]["max_word_length"]

    filtered_words = [
        word for word in words
        if len(word.replace("-", "")) <= max_length
    ]

    if not filtered_words:
        return words

    return filtered_words


def choose_random_word(word_categories, category, difficulty):
    words = word_categories[category]
    possible_words = filter_words_by_difficulty(words, difficulty)

    return random.choice(possible_words).lower()


def create_hint(answer):
    hint = []

    for character in answer:
        if character == "-":
            hint.append("-")
        else:
            hint.append("_")

    return hint


def display_man(wrong_guesses, hangman_art):
    print("\n**********")
    for line in hangman_art[wrong_guesses]:
        print(line)
    print("**********")


def display_hint(hint):
    print("Word:", " ".join(hint))


def display_guessed_letters(guessed_letters):
    if guessed_letters:
        print("Guessed letters:", ", ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters: None")


def display_answer(answer):
    print("Answer:", " ".join(answer))


def get_letter_guess(guessed_letters):
    while True:
        guess = input("Enter a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter one letter.")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        return guess


def get_hidden_letters(answer, hint):
    hidden_letters = []

    for index, character in enumerate(answer):
        if character.isalpha() and hint[index] == "_":
            hidden_letters.append(character)

    return list(set(hidden_letters))


def use_hint(answer, hint):
    hidden_letters = get_hidden_letters(answer, hint)

    if not hidden_letters:
        print("No hidden letters left to reveal.")
        return False

    revealed_letter = random.choice(hidden_letters)

    for index in range(len(answer)):
        if answer[index] == revealed_letter:
            hint[index] = revealed_letter

    print(f"Hint used! The letter '{revealed_letter}' has been revealed.")
    return True


def ask_use_hint(hints_left):
    if hints_left <= 0:
        return False

    while True:
        choice = input(f"Use a hint? You have {hints_left} left. (yes/no): ").lower().strip()

        if choice in ["yes", "y"]:
            return True

        if choice in ["no", "n"]:
            return False

        print("Please enter yes or no.")


def calculate_score(difficulty, wrong_guesses, hints_used, result):
    if result == "Lost":
        return 0

    base_scores = {
        "Easy": 100,
        "Medium": 150,
        "Hard": 200
    }

    score = base_scores[difficulty]
    score -= wrong_guesses * 10
    score -= hints_used * 15

    return max(0, score)


def save_game_result(player_name, category, difficulty, answer, result,
                     wrong_guesses, hints_used, score):
    stats = load_stats()

    game_result = {
        "player_name": player_name,
        "category": category,
        "difficulty": difficulty,
        "word": answer,
        "result": result,
        "wrong_guesses": wrong_guesses,
        "hints_used": hints_used,
        "score": score,
        "date_time": get_current_time()
    }

    stats.append(game_result)
    save_stats(stats)


def play_game(word_categories):
    player_name = get_player_name()
    category = choose_category(word_categories)
    difficulty = choose_difficulty()

    settings = DIFFICULTIES[difficulty]
    max_wrong_guesses = settings["max_wrong_guesses"]
    hints_left = settings["hints"]

    hangman_art = get_hangman_art(max_wrong_guesses)
    answer = choose_random_word(word_categories, category, difficulty)
    hint = create_hint(answer)

    wrong_guesses = 0
    hints_used = 0
    guessed_letters = set()

    print("\nGame Started!")
    print(f"Category: {category}")
    print(f"Difficulty: {difficulty}")
    print(f"Word Length: {len(answer.replace('-', ''))} letters")
    print("Hyphens are shown automatically if the word has them.")

    while True:
        display_man(wrong_guesses, hangman_art)
        display_hint(hint)
        display_guessed_letters(guessed_letters)

        print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")
        print(f"Hints left: {hints_left}")

        if ask_use_hint(hints_left):
            hint_used = use_hint(answer, hint)

            if hint_used:
                hints_left -= 1
                hints_used += 1

            if "_" not in hint:
                break

        guess = get_letter_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in answer:
            print(f"Good guess! '{guess}' is in the word.")

            for index in range(len(answer)):
                if answer[index] == guess:
                    hint[index] = guess
        else:
            print(f"Wrong guess. '{guess}' is not in the word.")
            wrong_guesses += 1

        if "_" not in hint:
            break

        if wrong_guesses >= max_wrong_guesses:
            break

    display_man(wrong_guesses, hangman_art)
    display_answer(answer)

    if "_" not in hint:
        result = "Won"
        print("YOU WIN!")
    else:
        result = "Lost"
        print("YOU LOSE!")

    score = calculate_score(difficulty, wrong_guesses, hints_used, result)

    print("\nGame Result")
    print("-" * 50)
    print(f"Player: {player_name}")
    print(f"Category: {category}")
    print(f"Difficulty: {difficulty}")
    print(f"Word: {answer}")
    print(f"Result: {result}")
    print(f"Wrong Guesses: {wrong_guesses}")
    print(f"Hints Used: {hints_used}")
    print(f"Score: {score}")

    save_game_result(
        player_name,
        category,
        difficulty,
        answer,
        result,
        wrong_guesses,
        hints_used,
        score
    )


def view_statistics():
    stats = load_stats()

    if not stats:
        print("\nNo statistics found yet.")
        return

    total_games = len(stats)
    wins = sum(1 for game in stats if game["result"] == "Won")
    losses = sum(1 for game in stats if game["result"] == "Lost")
    win_percentage = round((wins / total_games) * 100, 2)
    best_score = max(game["score"] for game in stats)
    average_score = round(sum(game["score"] for game in stats) / total_games, 2)

    category_counts = {}

    for game in stats:
        category = game["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

    favorite_category = max(category_counts, key=category_counts.get)

    print("\n" + "=" * 50)
    print("                 STATISTICS")
    print("=" * 50)
    print(f"Total Games Played: {total_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Percentage: {win_percentage}%")
    print(f"Best Score: {best_score}")
    print(f"Average Score: {average_score}")
    print(f"Favorite Category: {favorite_category}")
    print("=" * 50)

    print("\nRecent Games:")
    for index, game in enumerate(reversed(stats[-5:]), start=1):
        print(f"{index}. {game['player_name']} - {game['result']}")
        print(f"   Word: {game['word']}")
        print(f"   Category: {game['category']}")
        print(f"   Difficulty: {game['difficulty']}")
        print(f"   Score: {game['score']}")
        print(f"   Date: {game['date_time']}")
        print("-" * 50)


def view_word_categories(word_categories):
    print("\n" + "=" * 50)
    print("              WORD CATEGORIES")
    print("=" * 50)

    for category, words in word_categories.items():
        print(f"{category}: {len(words)} words")

    print("=" * 50)


def view_rules():
    print("\n" + "=" * 50)
    print("                  RULES")
    print("=" * 50)
    print("1. Choose a category and difficulty.")
    print("2. Guess one letter at a time.")
    print("3. Correct guesses reveal letters in the word.")
    print("4. Wrong guesses add to the hangman drawing.")
    print("5. You win if you reveal the full word.")
    print("6. You lose if you reach the wrong guess limit.")
    print("7. Hyphens are shown automatically.")
    print("8. Hints reveal one hidden letter but reduce your score.")
    print("=" * 50)


def ask_play_again():
    while True:
        choice = input("\nDo you want to play again? (yes/no): ").lower().strip()

        if choice in ["yes", "y"]:
            return True

        if choice in ["no", "n"]:
            return False

        print("Please enter yes or no.")


def main():
    word_categories = load_word_categories()

    if word_categories is None:
        return

    while True:
        display_main_menu()
        choice = get_menu_choice(["1", "2", "3", "4", "5"])

        if choice == "1":
            while True:
                play_game(word_categories)

                if not ask_play_again():
                    print("\nReturning to main menu...")
                    break

        elif choice == "2":
            view_statistics()

        elif choice == "3":
            view_word_categories(word_categories)

        elif choice == "4":
            view_rules()

        elif choice == "5":
            print("\nThanks for playing Advanced Hangman!")
            break


if __name__ == "__main__":
    main()
