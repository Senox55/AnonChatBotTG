import pytest


async def test_give_vip(db, duration, user_id):
    # Активируем VIP-доступ в базе данных
    await db.give_vip(user_id, duration=duration)
