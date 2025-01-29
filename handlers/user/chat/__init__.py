from aiogram import Router
from handlers.user.chat import (block_unblock, buy_vip, chat_utils, settings, next, process_chating, profile,
    registration, report_system, reputation_system, search, stop_dialog, stop_search)

user_chat_router = Router()

user_chat_router.include_router(stop_search.router)
user_chat_router.include_router(stop_dialog.router)
user_chat_router.include_router(buy_vip.router)
user_chat_router.include_router(reputation_system.router)
user_chat_router.include_router(report_system.router)
user_chat_router.include_router(registration.router)
user_chat_router.include_router(search.router)
user_chat_router.include_router(profile.router)
user_chat_router.include_router(settings.router)
user_chat_router.include_router(next.router)
user_chat_router.include_router(block_unblock.router)
user_chat_router.include_router(process_chating.router)
