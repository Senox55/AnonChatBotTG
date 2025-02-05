import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from redis.exceptions import RedisError

from app.tgbot.utils.utils import parse_user_info
from app.tgbot.states.registration import RegistrationFSM
from app.tgbot.keyboards import *

logger = logging.getLogger(__name__)


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Любое входящее сообщение проверяем:
        - Есть ли пол и возраст в базе?
        - Если нет, ставим пользователю FSM.fill_gender или fill_age
          (смотря, что отсутствует) и просим ввести.
        - И не даём идти дальше по хендлерам.
        """
        db = data["db"]
        redis = data["redis"]
        translator = data['translator']
        state = data["state"]

        user_data = await state.get_data()
        user_id = event.chat.id

        user_info = await redis.hgetall(name=f"users:{user_id}")

        logger.info(f"User {user_id} redis_data: {user_info}")

        if not user_info:
            logger.info(f"User {user_id} not found in Redis")
            user_info = parse_user_info(await db.get_user_info(user_id))

            logger.info(f"User {user_id} postgres_data: {user_info}")

            try:
                logger.info(f"User {user_id} parsed_data: {user_info}")
                await redis.hset(name=f"users:{user_id}", mapping=user_info)
                logger.info(f"User info stored in Redis for user ID: {user_id}")
            except RedisError as e:
                logger.error(f"Error storing user info in Redis for user ID: {user_id}: {e}")

        if not user_info:
            if not user_data.get('gender'):
                # Показываем сообщение про "выберите пол"
                await state.set_state(RegistrationFSM.FILL_GENDER)
                if event.text in (
                        ["Я Парень 🙋‍♂️", "Я Девушка 🙋‍♀️"]):
                    return await handler(event, data)
                await event.answer(translator.get('set_gender'),
                                   reply_markup=keyboard_before_set_gender)
                return  # Прерываем, чтобы не вызывать основной handler
            elif not user_data.get('age'):
                await state.set_state(RegistrationFSM.FILL_AGE)
                if event.text in (
                        ['📍 До 17', '📍 18-21', '📍 22-25', '📍 26-35', '📍 36-45', '📍 46+']):
                    return await handler(event, data)
                await event.answer(translator.get('set_age'),
                                   reply_markup=keyboard_before_set_age)
                return


        # Если всё нормально (либо зарегистрирован, либо уже внутри FSM), идём дальше.
        return await handler(event, data)
