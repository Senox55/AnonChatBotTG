from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from config_data.config import load_config
from keyboards import *

router = Router()
config = load_config('.env')


@router.callback_query(F.data == 'report')
async def process_choose_report_reason(callback: CallbackQuery, translator):
    await callback.message.edit_text(
        translator.get('choose_report_reason'),
        reply_markup=keyboard_reports_inline
    )


@router.callback_query(F.data == 'cancel_report')
async def process_cancel_report(callback: CallbackQuery, translator):
    await callback.message.edit_text(
        translator.get('evaluate_interlocutor'),
        reply_markup=keyboard_evaluate_interlocutor
    )


@router.callback_query(F.data.startswith('report_'))
async def process_report(callback: CallbackQuery, translator, db):
    # reporter_user_id = callback.from_user.id
    #
    # # reported_user_id =
    #
    # reason = callback.data.split('_')[1]
    #
    # db.send_report(reporter_user_id, reason)
    print(1)

    await callback.message.edit_text(
        translator.get('thanks_for_feedback'),
        reply_markup=None
    )
