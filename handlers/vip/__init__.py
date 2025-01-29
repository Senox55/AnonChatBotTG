from aiogram import Router
from handlers.vip.chat import vip_chat_router
from handlers.vip.games import vip_games_router

vip_router = Router()

vip_router.include_router(vip_games_router)
vip_router.include_router(vip_chat_router)