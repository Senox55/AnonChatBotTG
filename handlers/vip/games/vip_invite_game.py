from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.database import Database
from filters.is_in_chat_filter import IsINChat
from language.translator import Translator
from handlers.user.games.invite_games import process_invite_xo_game

router = Router()

@router.callback_query(F.data == "XO_mode_5", IsINChat())
async def process_invite_xo_game_5(callback: CallbackQuery, db: Database, translator: Translator):
    await process_invite_xo_game(callback, db, translator, 5)