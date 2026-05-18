from typing import Dict, Optional
from game.wordle import WordleGame, load_words

_WORD_LIST = load_words()
_sessions: Dict[int, WordleGame] = {}

def get_session(user_id: int) -> Optional[WordleGame]:
    return _sessions.get(user_id)

def start_session(user_id: int) -> WordleGame:
    game = WordleGame.new_game(_WORD_LIST)
    _sessions[user_id] = game
    return game

def clear_session(user_id: int) -> None:
    _sessions.pop(user_id, None)

def word_list_size() -> int:
    return len(_WORD_LIST)