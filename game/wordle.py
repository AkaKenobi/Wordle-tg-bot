import random
from dataclasses import dataclass, field
from typing import List, Optional

from config import MAX_ATTEMPTS, WORD_LENGTH, WORDS_FILE

CORRECT = "🟩"
PRESENT = "🟨"
ABSENT  = "⬛"

def load_words() -> List[str]:
    try:
        with open(WORDS_FILE, encoding="utf-8") as f:
            words = [line.strip().upper() for line in f if line.strip()]
        valid = [w for w in words if len(w) == WORD_LENGTH and w.isalpha()]
        return valid if valid else _fallback_words()
    except FileNotFoundError:
        return _fallback_words()

def _fallback_words() -> List[str]:
    return ["CRANE", "SLATE", "AUDIO", "RAISE", "AROSE",
            "STERN", "TRACE", "STARE", "SNARE", "IRATE"]

@dataclass
class GuessResult:
    word: str
    pattern: List[str]

    def as_string(self) -> str:
        return "".join(self.pattern) + f"  `{self.word}`"

class BaseGame:

    def __init__(self, secret: str, max_attempts: int):
        self.secret = secret
        self.max_attempts = max_attempts
        self.finished = False
        self.won = False

    def check_guess(self, guess: str):
        raise NotImplementedError("Subclasses must implement check_guess()")

    def board_as_text(self) -> str:
        raise NotImplementedError("Subclasses must implement board_as_text()")

    @property
    def attempts_left(self) -> int:
        raise NotImplementedError

    @property
    def attempts_used(self) -> int:
        raise NotImplementedError


class WordleGame(BaseGame):
    def __init__(self, secret: str, max_attempts: int = MAX_ATTEMPTS):
        super().__init__(secret, max_attempts)
        self.attempts: List[GuessResult] = []

    @classmethod
    def new_game(cls, word_list: List[str]) -> "WordleGame":
        secret = random.choice(word_list)
        return cls(secret=secret)

    @property
    def attempts_left(self) -> int:
        return self.max_attempts - len(self.attempts)

    @property
    def attempts_used(self) -> int:
        return len(self.attempts)

    def check_guess(self, guess: str) -> Optional[GuessResult]:
        guess = guess.upper()

        if len(guess) != WORD_LENGTH:
            return None

        pattern = self._build_pattern(guess)
        result = GuessResult(word=guess, pattern=pattern)
        self.attempts.append(result)

        if guess == self.secret:
            self.won = True
            self.finished = True
        elif len(self.attempts) >= self.max_attempts:
            self.finished = True

        return result

    def _build_pattern(self, guess: str) -> List[str]:
        pattern = [ABSENT] * WORD_LENGTH
        secret_remaining = list(self.secret)

        for i, (g, s) in enumerate(zip(guess, self.secret)):
            if g == s:
                pattern[i] = CORRECT
                secret_remaining[i] = None

        for i, g in enumerate(guess):
            if pattern[i] == CORRECT:
                continue
            if g in secret_remaining:
                pattern[i] = PRESENT
                secret_remaining[secret_remaining.index(g)] = None

        return pattern

    def board_as_text(self) -> str:
        lines = []
        for result in self.attempts:
            lines.append(result.as_string())
        return "\n".join(lines) if lines else "_(no guesses yet)_"