from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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

keyboard_choose_gender_search = ReplyKeyboardMarkup(keyboard=[[button_search_male, button_search_female]],
                                                    resize_keyboard=True)
