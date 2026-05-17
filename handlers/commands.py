from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from game import session
from game.stats import StatsManager
from config import MAX_ATTEMPTS, WORD_LENGTH

router = Router()
stats_manager = StatsManager()


@router.message(Command("start"))
async def cmd_start(message: Message):
    game = session.start_session(message.from_user.id)

    await message.answer(
        f"🟩 *Welcome to Wordle!*\n\n"
        f"I've chosen a secret *{WORD_LENGTH}-letter* English word.\n"
        f"You have *{MAX_ATTEMPTS} attempts*.\n\n"
        f"After each guess you'll see a hint:\n"
        f"🟩 — letter is in the correct spot\n"
        f"🟨 — letter is in the word but wrong spot\n"
        f"⬛ — letter is not in the word\n\n"
        f"Just type any {WORD_LENGTH}-letter word to guess!\n"
        f"_(dictionary: {session.word_list_size()} words)_",
        parse_mode="Markdown"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        f"📖 *How to play Wordle:*\n\n"
        f"• Guess a {WORD_LENGTH}-letter English word\n"
        f"• You have {MAX_ATTEMPTS} attempts\n"
        f"• After each guess you get a color-coded hint\n\n"
        f"*Commands:*\n"
        f"/start — start a new game\n"
        f"/stop — give up (reveal the word)\n"
        f"/stats — your statistics\n"
        f"/help — show this message",
        parse_mode="Markdown"
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    stats = stats_manager.get(message.from_user.id)
    await message.answer(stats.format(), parse_mode="Markdown")


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    game = session.get_session(message.from_user.id)

    if game is None or game.finished:
        await message.answer("No active game. Start one with /start")
        return

    secret = game.secret
    session.clear_session(message.from_user.id)
    stats_manager.record_result(message.from_user.id, won=False, attempts_used=game.attempts_used)

    await message.answer(
        f"🏳️ You gave up!\n"
        f"The secret word was: *{secret}*\n\n"
        f"Start again: /start",
        parse_mode="Markdown"
    )
