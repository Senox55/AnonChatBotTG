from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from config_data.config import load_config
from language.translator import Translator

router = Router()
config = load_config('.env')


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

