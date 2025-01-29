from aiogram import Router
from handlers.user.games import choose_games, game_xo, invite_games

user_games_router = Router()

user_games_router.include_router(choose_games.router)
user_games_router.include_router(game_xo.router)
user_games_router.include_router(invite_games.router)