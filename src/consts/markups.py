from telebot import types


class ButtonNames:
    help = "🆘Помощь🆘"
    start_learn = "👀Начать изучение👀"
    translator = "📱Переводчик📱"
    save_pair = "✍🏼Сохранить для изучения пару✍🏼"
    statistics = "✨Моя статистика✨"
    back_to_main = "🐾К основному меню🐾"
    get_all_words = "✨Получить мои слова✨"
    save_to_learn = "Сохранить для изучения"


def get_markup_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=ButtonNames.help)
    btn2 = types.KeyboardButton(text=ButtonNames.start_learn)
    btn3 = types.KeyboardButton(text=ButtonNames.translator)
    btn4 = types.KeyboardButton(text=ButtonNames.save_pair)
    btn5 = types.KeyboardButton(text=ButtonNames.statistics)
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def get_markup_save_words():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=ButtonNames.back_to_main)
    btn2 = types.KeyboardButton(text=ButtonNames.get_all_words)
    markup.add(btn1, btn2)
    return markup


def get_markup_translate():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=ButtonNames.back_to_main)
    btn2 = types.KeyboardButton(text=ButtonNames.save_to_learn)
    markup.add(btn1, btn2)
    return markup


def get_markup_translate_menu_to_word():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=ButtonNames.save_to_learn, callback_data="save_to_db")
    markup.add(btn1)
    return markup


def get_markup_back_to_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text=ButtonNames.back_to_main)
    markup.add(btn1)
    return markup
