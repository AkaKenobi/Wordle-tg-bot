from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from game import session
from game.stats import StatsManager
from config import MAX_ATTEMPTS, WORD_LENGTH

router = Router()
stats_manager = StatsManager()

def main_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 New Game"), KeyboardButton(text="📊 Stats")],
            [KeyboardButton(text="🏳️ Give Up"),  KeyboardButton(text="❓ Help")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def game_over_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Play Again", callback_data="new_game")],
        [InlineKeyboardButton(text="📊 My Stats",   callback_data="show_stats")],
    ])

@router.message(Command("start"))
@router.message(F.text == "🎮 New Game")
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
        parse_mode="Markdown",
        reply_markup=main_reply_keyboard()
    )


@router.message(Command("help"))
@router.message(F.text == "❓ Help")
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
        parse_mode="Markdown",
        reply_markup=main_reply_keyboard()
    )


@router.message(Command("stats"))
@router.message(F.text == "📊 Stats")
async def cmd_stats(message: Message):
    stats = stats_manager.get(message.from_user.id)
    await message.answer(
        stats.format(),
        parse_mode="Markdown",
        reply_markup=main_reply_keyboard()
    )


@router.message(Command("stop"))
@router.message(F.text == "🏳️ Give Up")
async def cmd_stop(message: Message):
    game = session.get_session(message.from_user.id)

    if game is None or game.finished:
        await message.answer(
            "No active game. Start one with /start",
            reply_markup=main_reply_keyboard()
        )
        return

    secret = game.secret
    session.clear_session(message.from_user.id)
    stats_manager.record_result(message.from_user.id, won=False, attempts_used=game.attempts_used)

    await message.answer(
        f"🏳️ You gave up!\n"
        f"The secret word was: *{secret}*\n\n"
        f"Start again: /start",
        parse_mode="Markdown",
        reply_markup=game_over_inline_keyboard()
    )

@router.callback_query(F.data == "new_game")
async def callback_new_game(callback: CallbackQuery):
    game = session.start_session(callback.from_user.id)
    await callback.message.answer(
        f"🟩 *New game started!*\n"
        f"I've chosen a secret *{WORD_LENGTH}-letter* word.\n"
        f"You have *{MAX_ATTEMPTS} attempts*. Good luck!",
        parse_mode="Markdown",
        reply_markup=main_reply_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "show_stats")
async def callback_show_stats(callback: CallbackQuery):
    stats = stats_manager.get(callback.from_user.id)
    await callback.message.answer(
        stats.format(),
        parse_mode="Markdown",
        reply_markup=main_reply_keyboard()
    )
    await callback.answer()
