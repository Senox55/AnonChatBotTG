from aiogram import Router
from handlers.vip.chat import search_gender, vip_command

vip_chat_router = Router()

vip_chat_router.include_router(search_gender.router)
vip_chat_router.include_router(vip_command.router)