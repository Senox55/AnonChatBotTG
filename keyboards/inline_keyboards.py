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

button_set_17 = InlineKeyboardButton(
    text='до 17 лет',
    callback_data='set_age_17'
)
button_set_21 = InlineKeyboardButton(
    text='от 18 до 21 года',
    callback_data='set_age_21'
)
button_set_25 = InlineKeyboardButton(
    text='от 22 до 25 лет',
    callback_data='set_age_25'
)
button_set_35 = InlineKeyboardButton(
    text='от 26 до 35 лет',
    callback_data='set_age_35'
)
button_set_45 = InlineKeyboardButton(
    text='от 36 до 45 лет',
    callback_data='set_age_45'
)
button_set_46 = InlineKeyboardButton(
    text='старше 46',
    callback_data='set_age_46'
)

button_buy_vip_for_7_days = InlineKeyboardButton(
    text="7 дней за 150 ⭐️",
    callback_data="buy_vip_stars_for_7_days")

button_buy_vip_for_1_month = InlineKeyboardButton(
    text="1 месяц за 250 ⭐️",
    callback_data="buy_vip_stars_for_1_month")

button_buy_vip_for_1_year = InlineKeyboardButton(
    text="1 год за 499 ⭐️",
    callback_data="buy_vip_stars_for_1_year")

keyboard_before_change_gender_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_male_inline, button_set_female_inline]])

keyboard_edit_profile_inline = InlineKeyboardMarkup(inline_keyboard=[[button_edit_profile_inline]])

keyboard_before_change_age_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_17, button_set_21, button_set_25],
                     [button_set_35, button_set_45, button_set_46]])

buy_vip_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [button_buy_vip_for_7_days],
    [button_buy_vip_for_1_month],
    [button_buy_vip_for_1_year]])
