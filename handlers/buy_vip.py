from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from config_data.config import load_config
from config_data.vip_config import VIP_CONFIG, PROVIDER_TOKEN, CURRENCY

router = Router()
config = load_config('.env')


@router.callback_query(F.data.startswith("buy_vip_stars_for_"))
async def process_buy_vip(callback: CallbackQuery, bot):
    # Получаем параметры для выбранного типа доступа
    data = callback.data.replace("buy_vip_stars_for_", "")
    vip_data = VIP_CONFIG[data]

    # Отправляем пользователю ссылку на оплату
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="VIP доступ",
        description=vip_data["description"],  # Описание из конфигов
        payload=f"vip_access_{data}",
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,  # Валюта из конфигов
        prices=[
            LabeledPrice(
                label=vip_data["label"],
                amount=vip_data["amount"]
            )
        ])


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot):
    # Подтверждаем готовность принять оплату
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(lambda message: message.successful_payment is not None)
async def process_successful_payment(message: Message, db, translator):
    """
    Обрабатываем успешный платеж.
    """
    # Получаем полезную нагрузку (payload) из успешного платежа
    payload = message.successful_payment.invoice_payload

    if "vip_access" in payload:
        vip_type = payload.replace("vip_access_", "")
        duration = VIP_CONFIG[vip_type]['duration']  # Извлекаем длительность из конфигов

        # Активируем VIP-доступ в базе данных
        await db.give_vip(message.from_user.id, duration=duration)

        await message.answer(translator.get("when_user_bought_vip"))
