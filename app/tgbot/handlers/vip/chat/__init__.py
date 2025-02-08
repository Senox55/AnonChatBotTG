from aiogram import Router
from app.tgbot.handlers.vip.chat import vip_command, search_gender, vip_search_settings

vip_chat_router = Router()

vip_chat_router.include_router(search_gender.router)
vip_chat_router.include_router(vip_command.router)
vip_chat_router.include_router(vip_search_settings.router)