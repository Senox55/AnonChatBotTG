from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from locales.translator import Translator

router = Router()


@router.callback_query(F.data == 'add_reputation')
async def process_add_reputation(callback: CallbackQuery, translator: Translator):
    """
    Функция для прибавления репутации пользователю
    :param callback:
    :param translator:
    :return:
    """
    await callback.message.edit_text(
        translator.get('thanks_for_feedback'), reply_markup=None
    )


@router.callback_query(F.data == 'reduce_reputation')
async def process_reduce_reputation(callback: CallbackQuery, translator: Translator):
    """
    Функция для убавления репутации пользователя
    :param callback:
    :param translator:
    :return:
    """
    await callback.message.edit_text(
        translator.get('thanks_for_feedback'),
        reply_markup=None
    )

