import json
import os
from dataclasses import dataclass, asdict
from typing import Dict

from config import STATS_FILE


@dataclass
class PlayerStats:
    games_played: int = 0
    games_won: int = 0
    current_streak: int = 0
    best_streak: int = 0
    total_attempts: int = 0

    @property
    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return round(self.games_won / self.games_played * 100, 1)

    @property
    def avg_attempts(self) -> float:
        if self.games_won == 0:
            return 0.0
        return round(self.total_attempts / self.games_won, 2)

    def record_win(self, attempts_used: int) -> None:
        self.games_played += 1
        self.games_won += 1
        self.current_streak += 1
        self.total_attempts += attempts_used
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak

    def record_loss(self) -> None:
        self.games_played += 1
        self.current_streak = 0

    def format(self) -> str:
        return (
            f"📊 *Your statistics:*\n"
            f"Games played: {self.games_played}\n"
            f"Wins: {self.games_won} ({self.win_rate}%)\n"
            f"Current streak: {self.current_streak} 🔥\n"
            f"Best streak: {self.best_streak}\n"
            f"Avg attempts per win: {self.avg_attempts}"
        )

class StatsManager:
    def __init__(self, filepath: str = STATS_FILE):
        self.filepath = filepath
        self._data: Dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}

    def _save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, user_id: int) -> PlayerStats:
        raw = self._data.get(str(user_id), {})
        return PlayerStats(**raw) if raw else PlayerStats()

    def update(self, user_id: int, stats: PlayerStats) -> None:
        self._data[str(user_id)] = asdict(stats)
        self._save()

    def record_result(self, user_id: int, won: bool, attempts_used: int) -> PlayerStats:
        stats = self.get(user_id)
        if won:
            stats.record_win(attempts_used)
        else:
            stats.record_loss()
        self.update(user_id, stats)
        return stats