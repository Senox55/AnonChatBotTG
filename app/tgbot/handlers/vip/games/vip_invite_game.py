from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.infrastructure.database.database import Database
from app.tgbot.filters.is_in_chat_filter import IsINChat
from locales.translator import Translator
from app.tgbot.handlers.user.games.invite_games import process_invite_xo_game

router = Router()

@router.callback_query(F.data == "XO_mode_5", IsINChat())
async def process_invite_xo_game_5(callback: CallbackQuery, db: Database, translator: Translator):
    await process_invite_xo_game(callback, db, translator, 5)