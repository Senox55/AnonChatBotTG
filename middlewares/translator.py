from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from copy import copy

from language.translator import Translator


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        new_data = copy(data)
        translator: Translator = new_data['translator']
        new_data['translator'] = translator(language="ru")
        return await handler(event, new_data)
