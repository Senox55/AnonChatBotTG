from aiogram import Router
from handlers.vip import vip_command, search_gender, vip_invite_game
from handlers.user import (stop_search, stop_dialog, buy_vip, reputation_system, report_system, registration,
                           process_chating, profile, edit_profile, choose_games, game_xo, invite_games, next,
                           block_unblock, search)

user_router = Router()
vip_router = Router()

user_router.include_router(stop_search.router)
user_router.include_router(stop_dialog.router)
user_router.include_router(buy_vip.router)
user_router.include_router(reputation_system.router)
user_router.include_router(report_system.router)
user_router.include_router(registration.router)
user_router.include_router(search.router)
user_router.include_router(profile.router)
user_router.include_router(edit_profile.router)
user_router.include_router(choose_games.router)
user_router.include_router(game_xo.router)
user_router.include_router(invite_games.router)
user_router.include_router(next.router)
user_router.include_router(block_unblock.router)
user_router.include_router(process_chating.router)

vip_router.include_router(vip_command.router)
vip_router.include_router(search_gender.router)
vip_router.include_router(vip_invite_game.router)
