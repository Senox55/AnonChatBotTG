from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from asyncpg import Pool

from database.database import Database


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, any]], Awaitable[None]],
            event: Update,
            data: dict[str, any]
    ) -> any:
        pool: Pool = data.get('_db_pool')

        async with pool.acquire() as connect:
            data['db'] = Database(connect)

            await handler(event, data)
