from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн-кнопка для редактирования профиля
button_edit_profile_inline = InlineKeyboardButton(
    text='⚙️ Изменить профиль',
    callback_data='edit_profile_pressed'
)

# Инлайн-кнопки для выбора пола
button_set_male_inline = InlineKeyboardButton(
    text='🙋‍♂️ Парень',
    callback_data='set_male_pressed'
)

button_set_female_inline = InlineKeyboardButton(
    text='🙋‍♀️ Девушка',
    callback_data='set_female_pressed'
)

# Инлайн-кнопки для выбора возраста
button_set_17_inline = InlineKeyboardButton(
    text='до 17',
    callback_data='set_age_17'
)
button_set_21_inline = InlineKeyboardButton(
    text='18-21',
    callback_data='set_age_21'
)
button_set_25_inline = InlineKeyboardButton(
    text='22-25',
    callback_data='set_age_25'
)
button_set_35_inline = InlineKeyboardButton(
    text='26-35',
    callback_data='set_age_35'
)
button_set_45_inline = InlineKeyboardButton(
    text='36-45',
    callback_data='set_age_45'
)
button_set_46_inline = InlineKeyboardButton(
    text='46+',
    callback_data='set_age_46'
)

button_buy_vip_for_7_days_inline = InlineKeyboardButton(
    text="👑 7 дней за 150 ⭐️",
    callback_data="buy_vip_stars_for_7_days")

button_buy_vip_for_1_month_inline = InlineKeyboardButton(
    text="👑 1 месяц за 250 ⭐️",
    callback_data="buy_vip_stars_for_1_month")

button_buy_vip_for_1_year_inline = InlineKeyboardButton(
    text="👑 1 год за 499 ⭐️",
    callback_data="buy_vip_stars_for_1_year")

button_two_members = InlineKeyboardButton(text='2️⃣', callback_data="set_room_capacity_2")

button_three_members = InlineKeyboardButton(text='3️⃣', callback_data="set_room_capacity_3")

button_four_members = InlineKeyboardButton(text='4️⃣', callback_data="set_room_capacity_4")

button_play_XO_inline = InlineKeyboardButton(text='🕹️ X-O', callback_data="invite_play_xo")

button_XO_mode_3_inline = InlineKeyboardButton(text='3x3', callback_data="XO_mode_3")

button_XO_mode_4_inline = InlineKeyboardButton(text='4x4', callback_data="XO_mode_4")

button_XO_mode_5_inline = InlineKeyboardButton(text='5x5 🔒', callback_data="XO_mode_5")

button_accept_game_inline = InlineKeyboardButton(text='✅ Принять', callback_data="accept_game")

button_refuse_game_inline = InlineKeyboardButton(text='❌ Отказаться', callback_data="refuse_game")

button_cancel_game_inline = InlineKeyboardButton(text='🚫 Отменить', callback_data="cancel_game")

button_report_inline = InlineKeyboardButton(text='⚠️ Пожаловаться', callback_data=f"report")

button_reduce_reputation = InlineKeyboardButton(text='👎', callback_data="reduce_reputation")

button_add_reputation = InlineKeyboardButton(text='👍', callback_data="add_reputation")

button_report_spam = InlineKeyboardButton(text='🤖 Спам', callback_data="report_spam")

button_report_abuse = InlineKeyboardButton(text='🤬 Оскорбления', callback_data="report_abuse")

button_report_content = InlineKeyboardButton(text='🔞 Контент', callback_data="report_content")

button_cancel_report_inline = InlineKeyboardButton(text='◀️Назад', callback_data="cancel_report")

edit_chat_mode = InlineKeyboardButton(text='🛡️ Режим безопасности', callback_data="change_chat_mode")

safe_mode = InlineKeyboardButton(text='🔒 Безопасный', callback_data="safe_mode")

unsafe_mode = InlineKeyboardButton(text='🔓 Без ограничений', callback_data="unsafe_mode")

keyboard_before_change_gender_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_set_male_inline, button_set_female_inline]])

keyboard_edit_settings_inline = InlineKeyboardMarkup(inline_keyboard=[[button_edit_profile_inline],
                                                                      [edit_chat_mode]])

keyboard_edit_chat_mode_inline = InlineKeyboardMarkup(inline_keyboard=[[safe_mode, unsafe_mode]])

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

keyboard_choose_game_mode_xo = InlineKeyboardMarkup(
    inline_keyboard=[[button_XO_mode_3_inline, button_XO_mode_4_inline, button_XO_mode_5_inline]])

keyboard_choose_room_capacity = InlineKeyboardMarkup(
    inline_keyboard=[[button_two_members, button_three_members, button_four_members]])
