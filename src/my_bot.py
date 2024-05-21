from googletrans import Translator
import telebot
from telebot import types

import settings
from consts import phrases
from generate_word import get_word_for_lesson
from database.dal.word_db import AllWordsData
from consts.markups import get_markup_main_menu, get_markup_save_words, ButtonNames, \
    get_markup_back_to_main_menu, get_markup_translate_menu_to_word
from database.dal.user_db import ClientData

translator = Translator()
db_words = ClientData()
db_all_words = AllWordsData()

bot = telebot.TeleBot(settings.TG_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup: types.ReplyKeyboardMarkup = get_markup_main_menu()
    bot.send_message(message.from_user.id, "Привет! Выбери действие)", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == ButtonNames.back_to_main)
def back_to_menu(message):
    markup: types.ReplyKeyboardMarkup = get_markup_main_menu()
    bot.send_message(message.from_user.id, "Выбери действие)", reply_markup=markup)


# ----------------------------------------функционал помощи

@bot.message_handler(func=lambda message: message.text == ButtonNames.help)
def help_from_menu(message):
    markup: types.ReplyKeyboardMarkup = get_markup_main_menu()
    bot.reply_to(message, phrases.help_text, reply_markup=markup)


# ----------------------------------------функционал сохранения

@bot.message_handler(func=lambda message: message.text == ButtonNames.save_pair)
def save_from_menu(message):
    markup = get_markup_save_words()

    sent = bot.reply_to(message, phrases.save_text, reply_markup=markup)
    bot.register_next_step_handler(sent, save_phrase)


def save_phrase(message):
    if message.text == ButtonNames.get_all_words:
        get_saved_words(message)
        return
    if message.text == ButtonNames.back_to_main:
        back_to_menu(message)
        return
    text = message.text.split('*')
    markup = get_markup_save_words()
    if len(text) != 2:
        sent = bot.send_message(message.from_user.id, f"Не получилось ввести( Проверь формат...", reply_markup=markup)
        bot.register_next_step_handler(sent, save_phrase)
        return
    db_words.insert_key(message.from_user.username, text[0], text[1])

    sent = bot.reply_to(message, f"Добавлена пара: \n'{text[0]}' -- '{text[1]}'.\n Можешь ввести что-то еще)",
                        reply_markup=markup)

    bot.register_next_step_handler(sent, save_phrase)


@bot.message_handler(func=lambda message: message.text == ButtonNames.get_all_words)
def get_saved_words(message):
    words = db_words.get_words(message.from_user.username)
    answer_words = ""
    for i in range(len(words)):
        answer_words += words[i][0] + ' - ' + words[i][1] + '\n'
    answer = f"Твои слова:\n{answer_words}"
    if answer_words == "":
        answer = "Их пока нет. Но можешь добавить по формату)"

    markup = get_markup_save_words()
    bot.reply_to(message, answer, reply_markup=markup)


# ----------------------------------------функционал перевода

@bot.message_handler(func=lambda message: message.text == ButtonNames.translator)
def translate_from_menu(message):
    markup = get_markup_back_to_main_menu()

    sent = bot.reply_to(message, phrases.translate_text, reply_markup=markup)
    bot.register_next_step_handler(sent, translate_phrase)


def translate_phrase(message):
    if message.text == ButtonNames.back_to_main:
        markup: types.ReplyKeyboardMarkup = get_markup_main_menu()
        bot.send_message(message.from_user.id, "Выбери действие)", reply_markup=markup)
        return
    text = translator.translate(message.text, dest='en').text
    sent = bot.reply_to(message, text, reply_markup=get_markup_translate_menu_to_word())
    bot.register_next_step_handler(sent, translate_phrase)


@bot.callback_query_handler(func=lambda call: call.data == "save_to_db")
def save_to_db_from_translate(callback):
    db_words.insert_key(callback.message.reply_to_message.from_user.username, callback.message.reply_to_message.text,
                        callback.message.text)

    markup = get_markup_back_to_main_menu()

    sent = bot.send_message(callback.message.reply_to_message.from_user.id, phrases.translate_text_next,
                            reply_markup=markup)
    bot.register_next_step_handler(sent, translate_phrase)


# ----------------------------------------функционал урока

@bot.message_handler(func=lambda message: message.text == ButtonNames.start_learn)
def start_learn(message):
    markup = get_markup_back_to_main_menu()
    bot.send_message(message.from_user.id, phrases.start_lesson_text,
                     reply_markup=markup)
    send_next_step(message, [])


def send_next_step(message, words):
    word = get_word_for_lesson(message.from_user.username)
    markup = get_markup_back_to_main_menu()
    sent = bot.send_message(message.from_user.id, f"Напиши перевод для: {word[0]}.",
                            reply_markup=markup)
    bot.register_next_step_handler(sent, check_cur_step, word, words)


def check_cur_step(message, word, words):
    if message.text == ButtonNames.back_to_main:
        for w in words:
            db_words.insert_key(message.from_user.username, w[0], w[1])
        db_words.insert_key(message.from_user.username, word[0], word[1])
        back_to_menu(message)
        return
    if message.text.lower().strip() == word[1].lower().strip():
        bot.reply_to(message, f"Поздравляю! Верно)",
                     reply_markup=get_markup_back_to_main_menu())
        send_next_step(message, words)
        return
    else:
        words.append(word)
        bot.reply_to(message, f"Не верно(\n{word[0]} -- {word[1]}.", reply_markup=get_markup_back_to_main_menu())
        send_next_step(message, words)
        return


# ----------------------------------------функционал статистики

@bot.message_handler(func=lambda message: message.text == ButtonNames.statistics)
def statistics(message):
    markup = get_markup_main_menu()
    bot.send_message(message.from_user.id, f"Слов для изучения: {len(db_words.get_words(message.from_user.username))}.",
                     reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
