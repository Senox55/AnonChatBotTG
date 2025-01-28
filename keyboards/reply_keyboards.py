from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_search_random = KeyboardButton(text='🎭 Найти маску')
button_search_by_gender = KeyboardButton(text='👫Поиск по полу')
button_stop_search = KeyboardButton(text='✋ Отменить поиск')
button_stop_dialog = KeyboardButton(text='👋 Завершить чат')
button_set_male = KeyboardButton(text='Я Парень 🙋‍♂️')
button_set_female = KeyboardButton(text='Я Девушка 🙋‍♀️')
button_search_male = KeyboardButton(text='Найти Парня 🙋‍♂️')
button_search_female = KeyboardButton(text='Найти Девушку 🙋‍♀️')
button_profile = KeyboardButton(text='👤 Профиль')
button_cancel_choose_gender_for_search = KeyboardButton(text='↩️ Назад')
button_age_less_17 = KeyboardButton(text='📍 До 17')
button_age_between_18_21 = KeyboardButton(text='📍 18-21')
button_age_between_22_25 = KeyboardButton(text='📍 22-25')
button_age_between_26_35 = KeyboardButton(text='📍 26-35')
button_age_between_36_45 = KeyboardButton(text='📍 36-45')
button_age_more_46 = KeyboardButton(text='📍 46+')
button_start_play = KeyboardButton(text='🎲 Играть')

keyboard_before_start_search = ReplyKeyboardMarkup(
    keyboard=[[button_search_random],
              [button_search_by_gender],
              [button_profile]], resize_keyboard=True, row_width=1)

keyboard_after_start_research = ReplyKeyboardMarkup(keyboard=[[button_stop_search]], resize_keyboard=True)

keyboard_after_find_dialog = ReplyKeyboardMarkup(keyboard=[[button_stop_dialog],
                                                           [button_start_play]], resize_keyboard=True)

keyboard_before_set_gender = ReplyKeyboardMarkup(keyboard=[[button_set_male, button_set_female]], resize_keyboard=True)

keyboard_before_set_age = ReplyKeyboardMarkup(
    keyboard=[[button_age_less_17, button_age_between_18_21, button_age_between_22_25],
              [button_age_between_26_35, button_age_between_36_45, button_age_more_46]], resize_keyboard=True)

keyboard_choose_gender_search = ReplyKeyboardMarkup(keyboard=[[button_search_male, button_search_female],
                                                              [button_cancel_choose_gender_for_search]],
                                                    resize_keyboard=True)
