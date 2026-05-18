from aiogram import Router
from aiogram.types import Message

from game import session
from game.stats import StatsManager
from config import WORD_LENGTH
from handlers.commands import main_reply_keyboard, game_over_inline_keyboard

router = Router()
stats_manager = StatsManager()


@router.message()
async def handle_guess(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    game = session.get_session(user_id)
    if game is None:
        await message.answer(
            "No active game. Start one with /start 🎮",
            reply_markup=main_reply_keyboard()
        )
        return

    if game.finished:
        await message.answer(
            "The game is already over. Start a new one: /start",
            reply_markup=main_reply_keyboard()
        )
        return

    if len(text) != WORD_LENGTH:
        await message.answer(f"⚠️ Please enter exactly {WORD_LENGTH} letters. Try again!")
        return

    if not text.isalpha():
        await message.answer("⚠️ Letters only — no digits or symbols.")
        return

    result = game.check_guess(text)
    if result is None:
        await message.answer("Something went wrong. Please try again.")
        return

    board = game.board_as_text()

    if game.won:
        session.clear_session(user_id)
        updated_stats = stats_manager.record_result(user_id, won=True, attempts_used=game.attempts_used)

        await message.answer(
            f"{board}\n\n"
            f"🎉 *Correct! You guessed it in {game.attempts_used} attempt{'s' if game.attempts_used != 1 else ''}!*\n\n"
            f"{updated_stats.format()}\n\n"
            f"Want to play again?",
            parse_mode="Markdown",
            reply_markup=game_over_inline_keyboard()
        )

    elif game.finished:
        session.clear_session(user_id)
        updated_stats = stats_manager.record_result(user_id, won=False, attempts_used=game.attempts_used)

        await message.answer(
            f"{board}\n\n"
            f"😔 *Out of attempts!*\n"
            f"The secret word was: *{game.secret}*\n\n"
            f"{updated_stats.format()}",
            parse_mode="Markdown",
            reply_markup=game_over_inline_keyboard()
        )

    else:
        await message.answer(
            f"{board}\n\n"
            f"_Attempts remaining: {game.attempts_left}_",
            parse_mode="Markdown",
            reply_markup=main_reply_keyboard()
        )
