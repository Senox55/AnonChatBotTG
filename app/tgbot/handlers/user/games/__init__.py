from aiogram import Router
from app.tgbot.handlers.user.games import choose_games, invite_games
from app.tgbot.handlers.user.games import game_xo

user_games_router = Router()

user_games_router.include_router(choose_games.router)
user_games_router.include_router(game_xo.router)
user_games_router.include_router(invite_games.router)