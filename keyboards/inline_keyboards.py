from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-кнопка для редактирования профиля
button_edit_profile_inline = InlineKeyboardButton(
    text='⚙️ Изменить профиль',
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

button_set_17_inline = InlineKeyboardButton(
    text='до 17 лет',
    callback_data='set_age_17'
)
button_set_21_inline = InlineKeyboardButton(
    text='от 18 до 21 года',
    callback_data='set_age_21'
)
button_set_25_inline = InlineKeyboardButton(
    text='от 22 до 25 лет',
    callback_data='set_age_25'
)
button_set_35_inline = InlineKeyboardButton(
    text='от 26 до 35 лет',
    callback_data='set_age_35'
)
button_set_45_inline = InlineKeyboardButton(
    text='от 36 до 45 лет',
    callback_data='set_age_45'
)
button_set_46_inline = InlineKeyboardButton(
    text='старше 46',
    callback_data='set_age_46'
)

button_buy_vip_for_7_days_inline = InlineKeyboardButton(
    text="7 дней за 150 ⭐️",
    callback_data="buy_vip_stars_for_7_days")

button_buy_vip_for_1_month_inline = InlineKeyboardButton(
    text="1 месяц за 250 ⭐️",
    callback_data="buy_vip_stars_for_1_month")

button_buy_vip_for_1_year_inline = InlineKeyboardButton(
    text="1 год за 499 ⭐️",
    callback_data="buy_vip_stars_for_1_year")

button_play_XO_inline = InlineKeyboardButton(text='X-O', callback_data="invite_play_xo")

button_accept_game_inline = InlineKeyboardButton(text='Принять', callback_data="accept_game")

button_refuse_game_inline = InlineKeyboardButton(text='Отказаться', callback_data="refuse_game")

button_cancel_game_inline = InlineKeyboardButton(text='Отменить', callback_data="cancel_game")

button_report_inline = InlineKeyboardButton(text='⚠️Пожаловаться', callback_data=f"report")

button_reduce_reputation = InlineKeyboardButton(text='👎', callback_data="reduce_reputation")

button_add_reputation = InlineKeyboardButton(text='👍', callback_data="add_reputation")

button_report_spam = InlineKeyboardButton(text='🤖Спам', callback_data="report_spam")

button_report_abuse = InlineKeyboardButton(text='🤬Оскорбления', callback_data="report_abuse")

button_report_content = InlineKeyboardButton(text='🔞Неприемлемый контент', callback_data="report_content")

button_cancel_report_inline = InlineKeyboardButton(text='◀️Назад', callback_data="cancel_report")

keyboard_before_change_gender_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_male_inline, button_set_female_inline]])

keyboard_edit_profile_inline = InlineKeyboardMarkup(inline_keyboard=[[button_edit_profile_inline]])

keyboard_before_change_age_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_17_inline, button_set_21_inline, button_set_25_inline],
                     [button_set_35_inline, button_set_45_inline, button_set_46_inline]])

buy_vip_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [button_buy_vip_for_7_days_inline],
    [button_buy_vip_for_1_month_inline],
    [button_buy_vip_for_1_year_inline]])

keyboard_before_choose_game_inline = InlineKeyboardMarkup(inline_keyboard=[[button_play_XO_inline]])

keyboard_before_accept_game_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_accept_game_inline, button_refuse_game_inline]])

keyboard_before_cancel_game_inline = InlineKeyboardMarkup(inline_keyboard=[[button_cancel_game_inline]])

keyboard_evaluate_interlocutor = InlineKeyboardMarkup(
    inline_keyboard=[[button_add_reputation, button_reduce_reputation], [button_report_inline]])

keyboard_reports_inline = InlineKeyboardMarkup(inline_keyboard=[[button_report_spam],
                                                                [button_report_abuse],
                                                                [button_report_content],
                                                                [button_cancel_report_inline]])
