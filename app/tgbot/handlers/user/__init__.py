from aiogram import Router
from app.tgbot.handlers.user.games import user_games_router
from app.tgbot.handlers.user.chat import user_chat_router

user_router = Router()

# user_router.include_router(user_games_router)
user_router.include_router(user_chat_router)