from aiogram import Router
from app.tgbot.handlers.vip.chat import vip_command
from app.tgbot.handlers.vip.chat import search_gender

vip_chat_router = Router()

vip_chat_router.include_router(search_gender.router)
vip_chat_router.include_router(vip_command.router)