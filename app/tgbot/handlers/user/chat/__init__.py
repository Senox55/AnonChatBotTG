from aiogram import Router
from app.tgbot.handlers.user.chat import (block_unblock, buy_vip, settings, next, process_chating, profile,
                                          registration, reputation_system, search, stop_dialog, stop_search,
                                          search_setting, edit_profile)
from app.tgbot.handlers.user.chat import report_system

user_chat_router = Router()

user_chat_router.include_router(stop_search.router)
user_chat_router.include_router(stop_dialog.router)
user_chat_router.include_router(buy_vip.router)
user_chat_router.include_router(reputation_system.router)
user_chat_router.include_router(report_system.router)
user_chat_router.include_router(registration.router)
user_chat_router.include_router(search_setting.router)
user_chat_router.include_router(search.router)
user_chat_router.include_router(profile.router)
user_chat_router.include_router(edit_profile.router)
user_chat_router.include_router(settings.router)
user_chat_router.include_router(next.router)
user_chat_router.include_router(block_unblock.router)
user_chat_router.include_router(process_chating.router)
