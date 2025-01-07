from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import Database
from config import bot_token
from functools import wraps

BOT_TOKEN = bot_token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = Database()

button_edit_profile_inline = InlineKeyboardButton(
    text='Изменить профиль',
    callback_data='edit_profile_pressed'
)

button_set_male_inline = InlineKeyboardButton(
    text='Я Парень 🙋‍♂',
    callback_data='set_male_pressed'
)

button_set_female_inline = InlineKeyboardButton(
    text='Я Девушка 🙋‍♀️',
    callback_data='set_female_pressed'
)

button_search_random = KeyboardButton(text='🔍Начать общение')
button_search_by_gender = KeyboardButton(text='👫Поиск по полу')
button_stop_search = KeyboardButton(text='✋ Остановить поиск')
button_stop_dialog = KeyboardButton(text='❌ Завершить диалог')
button_set_male = KeyboardButton(text='Я Парень 🙋‍♂️')
button_set_female = KeyboardButton(text='Я Девушка 🙋‍♀️')
button_search_male = KeyboardButton(text='Найти Парня 🙋‍♂️')
button_search_female = KeyboardButton(text='Найти Девушку 🙋‍♀️')
button_profile = KeyboardButton(text='👤 Профиль')

keyboard_before_start_search = ReplyKeyboardMarkup(
    keyboard=[[button_search_random],
              [button_search_by_gender],
              [button_profile]], resize_keyboard=True, row_width=1)

keyboard_after_start_research = ReplyKeyboardMarkup(keyboard=[[button_stop_search]], resize_keyboard=True)
keyboard_after_find_dialog = ReplyKeyboardMarkup(keyboard=[[button_stop_dialog]], resize_keyboard=True)
keyboard_before_set_gender = ReplyKeyboardMarkup(keyboard=[[button_set_male, button_set_female]], resize_keyboard=True)

keyboard_before_change_gender_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_male_inline, button_set_female_inline]])

keyboard_edit_profile_inline = InlineKeyboardMarkup(inline_keyboard=[[button_edit_profile_inline]])

keyboard_choose_gender_search = ReplyKeyboardMarkup(keyboard=[[button_search_male, button_search_female]],
                                                    resize_keyboard=True)


def gender_required(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        setted_gender = await db.get_gender(message.chat.id)
        if not setted_gender:
            await message.answer(
                'Для начала работы укажите ваш пол: ',
                reply_markup=keyboard_before_set_gender
            )
            return
        return await func(message, *args, **kwargs)

    return wrapper


async def start_search(message: Message, desired_gender: str = 'anon'):
    """
    Универсальная функция для начала поиска собеседника.

    :param message: Объект сообщения пользователя.
    :param desired_gender: Пол собеседника, которого ищет пользователь ('male', 'female', 'anon').
    """
    user_info = await db.get_chat(desired_gender)
    chat_two = user_info[0]
    gender = user_info[1]
    desired_gender_of_other = user_info[2]  # Пол, который ищет другой пользователь

    is_in_queue = await db.is_in_queue(message.chat.id)
    chat_info = await db.get_active_chat(message.chat.id)

    if not is_in_queue:
        if not chat_info:
            if (message.chat.id == chat_two
                    or user_info == [0]
                    or (desired_gender_of_other != 'anon' and await db.get_gender(
                        message.chat.id) != desired_gender_of_other)
                    or not await db.create_chat(message.chat.id, chat_two)):

                await db.add_queue(message.chat.id, await db.get_gender(message.chat.id), desired_gender)
                await message.answer(
                    'Ищем собеседника... 🔍\n\n'
                    'Пожалуйста, подождите немного — мы уже подбираем для вас интересного человека. 😊',
                    reply_markup=keyboard_after_start_research
                )
            else:
                mess = '''🎉 Ура! Собеседник найден! \n\nНачинайте общение прямо сейчас.\n/next — искать нового собеседника\n/stop — закончить диалог'''
                await bot.send_message(
                    message.chat.id,
                    mess,
                    reply_markup=keyboard_after_find_dialog
                )
                await bot.send_message(
                    chat_two,
                    mess,
                    reply_markup=keyboard_after_find_dialog
                )
        else:
            await message.answer(
                "У вас уже есть собеседник 🤔\n/next — искать нового собеседника\n/stop — закончить диалог",
                reply_markup=keyboard_after_find_dialog
            )

    else:
        await message.answer(
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )


@dp.message(CommandStart())
@gender_required
async def process_start_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(Command(commands=['search']))
@gender_required
async def process_start_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(Command(commands=['next']))
@gender_required
async def process_start_command(message: Message, desired_gender='anon'):
    chat_info = await db.get_active_chat(message.chat.id)
    if chat_info:
        await db.delete_chat(chat_info[0])
        await bot.send_message(
            message.chat.id,
            "Вы покинули чат ❌",
            reply_markup=keyboard_before_start_search,
        )
        await bot.send_message(
            chat_info[1],
            "Ваш собеседник завершил диалог ❌",
            reply_markup=keyboard_before_start_search
        )

    user_info = await db.get_chat(desired_gender)
    chat_two = user_info[0]
    gender = user_info[1]
    desired_gender_of_other = user_info[2]  # Пол, который ищет другой пользователь

    is_in_queue = await db.is_in_queue(message.chat.id)

    if not is_in_queue:
        if (message.chat.id == chat_two
                or user_info == [0]
                or (desired_gender_of_other != 'anon' and await db.get_gender(
                    message.chat.id) != desired_gender_of_other)
                or not await db.create_chat(message.chat.id, chat_two)):

            await db.add_queue(message.chat.id, await db.get_gender(message.chat.id), desired_gender)
            await message.answer(
                'Ищем собеседника... 🔍\n\n'
                'Пожалуйста, подождите немного — мы уже подбираем для вас интересного человека. 😊',
                reply_markup=keyboard_after_start_research
            )
        else:
            mess = '''🎉 Ура! Собеседник найден! \n\nНачинайте общение прямо сейчас.\n/next — искать нового собеседника\n/stop — закончить диалог'''
            await bot.send_message(
                message.chat.id,
                mess,
                reply_markup=keyboard_after_find_dialog
            )
            await bot.send_message(
                chat_two,
                mess,
                reply_markup=keyboard_after_find_dialog
            )
    else:
        await message.answer(
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )


@dp.message(F.text == '👫Поиск по полу')
@gender_required
async def process_choose_gender_search(message: Message):
    await message.answer(
        'Выберите желаемый пол собеседника:',
        reply_markup=keyboard_choose_gender_search
    )


@dp.message(F.text == '🔍Начать общение')
@gender_required
async def process_start_search_random_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(F.text == 'Найти Парня 🙋‍♂️')
@gender_required
async def process_start_search_male_command(message: Message):
    await start_search(message, desired_gender='male')


@dp.message(F.text == 'Найти Девушку 🙋‍♀️')
@gender_required
async def process_start_search_male_command(message: Message):
    await start_search(message, desired_gender='female')


async def stop_dialog(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
    if chat_info:
        await increment_chat_count(message.chat.id)
        await increment_chat_count(chat_info[1])

        await db.delete_chat(chat_info[0])

        await bot.send_message(
            message.chat.id,
            "Вы покинули чат ❌",
            reply_markup=keyboard_before_start_search,
        )
        await bot.send_message(
            chat_info[1],
            "Ваш собеседник завершил диалог ❌",
            reply_markup=keyboard_before_start_search
        )
    else:
        is_in_queue = await db.is_in_queue(message.chat.id)
        if is_in_queue:
            await db.delete_queue(message.chat.id)
            await message.answer(
                '🔕 Поиск отменён.',
                reply_markup=keyboard_before_start_search
            )
        else:
            await message.answer(
                '⚠ Вы не находитесь в диалоге.\n'
                'Напишите /search, чтобы найти собеседника',
                reply_markup=keyboard_before_start_search
            )


@dp.message(Command(commands=['stop']))
@gender_required
async def process_stop_command(message: Message):
    await stop_dialog(message)


@dp.message(F.text == '❌ Завершить диалог')
@gender_required
async def process_stop_button(message: Message):
    await stop_dialog(message)


@dp.message(F.text == '✋ Остановить поиск')
@gender_required
async def process_finish_search_command(message: Message):
    # Проверяем, находится ли пользователь в очереди
    is_in_queue = await db.is_in_queue(message.chat.id)

    if is_in_queue:
        # Удаляем пользователя из очереди, если он в поиске
        await db.delete_queue(message.chat.id)
        await message.answer(
            'Поиск отменён',
            reply_markup=keyboard_before_start_search
        )
    else:
        # Уведомляем, что пользователь не в поиске
        await message.answer(
            'Вы не находитесь в поиске.',

            reply_markup=keyboard_before_start_search
        )


@dp.message(F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']))
async def set_gender(message: Message):
    if not await db.get_user_info(message.chat.id):
        if message.text == 'Я Парень 🙋‍♂️':
            gender = 'male'
        elif message.text == 'Я Девушка 🙋‍♀️':
            gender = 'female'
        else:
            return  # Если сообщение не соответствует ожиданиям, ничего не делаем

        # Сохраняем пол в базу данных
        await db.set_gender(message.chat.id, gender)

        # Отправляем приветственное сообщение и клавиатуру для дальнейшего взаимодействия
        await message.answer(
            'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
            reply_markup=keyboard_before_start_search
        )


@dp.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery):
    await db.update_gender(callback.message.chat.id, 'male')
    await callback.message.edit_text(
        'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
        reply_markup=None)


@dp.callback_query(F.data == 'set_female_pressed')
async def process_set_male_gender(callback: CallbackQuery):
    await db.update_gender(callback.message.chat.id, 'female')
    await callback.message.edit_text(
        'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
        reply_markup=None)


async def increment_chat_count(user_id: int):
    await db.increment_chat_count(user_id)


async def show_profile(message: Message):
    user_id = message.chat.id
    user_info = await db.get_user_info(user_id)

    if user_info:
        chat_count = user_info[3]
        gender = user_info[2]

        profile_message = (
            f"<b>Ваш профиль</b>\n\n"
            f"💬 Чатов — {chat_count}\n"
            f"Пол — {gender}\n\n"
            "Выберите, что вы хотите изменить:"
        )

        await message.answer(profile_message, parse_mode="HTML", reply_markup=keyboard_edit_profile_inline)


@dp.message(Command(commands=['profile']))
@gender_required
async def process_profile_command(message: Message):
    await show_profile(message)


@dp.message(F.text == '👤 Профиль')
@gender_required
async def process_profile_button(message: Message):
    await show_profile(message)


@dp.callback_query(F.data == 'edit_profile_pressed')
async def process_button_2_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='1.Укажите ваш пол:',
        reply_markup=keyboard_before_change_gender_inline
    )


# Определение состояний
class GenderChange(StatesGroup):
    waiting_for_gender = State()


@dp.message(lambda message: message.text in ['Изменить пол'])
async def change_gender(message: Message, state: FSMContext):
    await message.answer(
        "Выберите ваш пол:\n"
        "Мужчина \n"
        "Женщина",
        reply_markup=keyboard_before_change_gender_inline
    )
    await state.set_state(GenderChange.waiting_for_gender)


@dp.message(GenderChange.waiting_for_gender)
async def set_gender_for_profile(message: Message, state: FSMContext):
    if message.text == 'Мужчина':
        gender = 'male'
    elif message.text == 'Женщина':
        gender = 'female'
    else:
        return  # Если сообщение не соответствует ожиданиям, ничего не делаем

    # Обновляем пол в базе данных
    await db.update_gender(message.chat.id, gender)

    # Отправляем подтверждение и возвращаемся к редактированию профиля
    await message.answer(
        'Ваш пол успешно изменён!',
        reply_markup=keyboard_before_start_search
    )
    await state.clear()


@dp.message()
@gender_required
async def process_chatting(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
    is_in_queue = await db.is_in_queue(message.chat.id)
    if chat_info:
        await message.send_copy(chat_id=chat_info[1])
    elif is_in_queue:
        await message.answer(
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )
    else:
        await message.answer(
            'Вы еще не начали диалог',
            reply_markup=keyboard_before_start_search
        )


if __name__ == '__main__':
    dp.run_polling(bot)
