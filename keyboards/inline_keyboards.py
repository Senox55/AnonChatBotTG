from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-кнопка для редактирования профиля
button_edit_profile_inline = InlineKeyboardButton(
    text='Изменить профиль',
    callback_data='edit_profile_pressed'
)

# Инлайн-кнопки для выбора пола
button_set_male_inline = InlineKeyboardButton(
    text='Я Парень 🙋‍♂',
    callback_data='set_male_pressed'
)

button_set_female_inline = InlineKeyboardButton(
    text='Я Девушка 🙋‍♀️',
    callback_data='set_female_pressed'
)

keyboard_before_change_gender_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_male_inline, button_set_female_inline]])

keyboard_edit_profile_inline = InlineKeyboardMarkup(inline_keyboard=[[button_edit_profile_inline]])
