# 🟩 WORDLE TELEGRAM BOT

## 1. Project Overview
Wordle Bot is a Telegram bot built with Python and the aiogram 3 framework. 
The bot challenges players to guess a secret 5-letter English word within 6 attempts.

After each guess, the bot responds with a color-coded hint:
* 🟩 - Letter is in the correct position
* 🟨 - Letter is in the word but wrong position
* ⬛ - Letter is not in the word at all

## 2. Features
* `/start` - begins a new game with a random secret word
* `/stop` - surrenders the current game and reveals the secret word
* `/stats` - displays the player's personal statistics
* `/help` - shows the rules and available commands
* Color-coded emoji hints after every guess
* Correct handling of duplicate letters (same logic as the original NYT Wordle)
* Player statistics saved to a JSON file between sessions

## 3. Technology Stack
* **Language:** Python 3.10+
* **Bot Framework:** aiogram 3.x (Telegram Bot API)
* **Data Storage:** JSON file (stats.json)
* **Architecture:** OOP - classes `WordleGame`, `PlayerStats`, `StatsManager`
* **Word Dictionary:** Plain text file (words.txt), 349 words

## 4. Project Structure
```text
wordle_bot/
├── bot.py
├── config.py
├── requirements.txt
├── data/
│   ├── words.txt
│   └── stats.json
├── game/
│   ├── wordle.py
│   ├── stats.py
│   └── session.py
└── handlers/
    ├── commands.py
    └── game_handler.py
```
    
5. Installation & Setup  

Step 1   
Open Telegram, find @BotFather, send /newbot and follow the prompts. Copy the token you receive.   

Step 2   
git clone https://github.com/AkaKenobi/Wordle-tg-bot.git
cd wordle-bot

Step 3   
pip install -r requirements.txt

Step 4   
Open config.py and replace the placeholder with token:   

Python
BOT_TOKEN = "Token"

Step 5   
python bot.py

The bot is now live. Open Telegram, find bot, and send /start.

6. Team Responsibilities   

* Ramazan – wordle.py / config.py / session.py   
* Islam – bot.py / game_handler.py   
* Yerassyl – commands.py / stats.py

7. OOP Design   

The project uses object-oriented programming throughout all core modules.
Classes:
* BaseGame (game/wordle.py) - The base class for word-guessing games. Stores the secret word, attempt limit, and game state (finished, won). Defines the interface that all subclasses must implement.   
* WordleGame (game/wordle.py) - Inherits from BaseGame. Implements the full Wordle game logic including guess validation, emoji hint generation, and board display. Overrides check_guess() and board_as_text() from the base class.   
* GuessResult (game/wordle.py) - A dataclass that stores a single guess word and its emoji pattern result.   
* PlayerStats (game/stats.py) - A dataclass that tracks a player's games played, wins, current streak, best streak, and total attempts. Win rate and average attempts are computed dynamically using @property.   
* StatsManager (game/stats.py) - Manages statistics for all players. Reads data from stats.json on startup and writes it back after every game.

OOP Concepts Used:   
* Inheritance - WordleGame inherits from BaseGame using super().__init__(), reusing the base state fields.   
* Polymorphism - check_guess() and board_as_text() are declared in BaseGame and overridden in WordleGame.   
* Encapsulation - StatsManager keeps internal data private (_data, _load(), _save()).   
* @dataclass - GuessResult and PlayerStats use the `@dataclass decorator to auto-generate init and repr.   
* @classmethod - WordleGame.new_game() is a factory method that creates a game instance from a word list.   
* @property - win_rate, avg_attempts, attempts_left, and attempts_used are computed on the fly without storing extra fields.

8. Data Persistence 

Player statistics are stored in data/stats.json. The file is created automatically on first run. Example structure:   
```text
JSON
{
  "123456789": {
    "games_played": 10,
    "games_won": 7,
    "current_streak": 3,
    "best_streak": 5,
    "total_attempts": 28
  }
}
```
The word list is loaded from data/words.txt at startup. If the file is missing, a built-in fallback list of 10 words is used automatically.
9. Possible Extensions  

Difficulty levels (4, 5, 6 letters)   
Leaderboard   
Russian language support   
Inline mode