from aiogram.filters import Filter
from aiogram import types
from datetime import datetime


class IsVIP(Filter):
    async def __call__(self, message: types.Message, db) -> bool:
        user_id = message.chat.id
        vip_status = await db.get_vip_status(user_id)
        if vip_status:
            # Если статус найден, проверяем, истёк ли он
            end_date = vip_status['end_date']
            if end_date and end_date < datetime.now().date():
                print(1)
                # Если срок действия истёк, деактивируем статус
                await db.deactivate_vip_status(user_id)
                return False  # Статус больше не активен
            return True  # Статус активен

            # Если статуса нет, возвращаем False
        return False
