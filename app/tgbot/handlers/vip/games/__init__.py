from aiogram import Router
from app.tgbot.handlers.vip.games import vip_invite_game

vip_games_router = Router()

vip_games_router.include_router(vip_invite_game.router)