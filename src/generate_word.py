from random import random

from database.dal.word_db import AllWordsData
from database.dal.user_db import ClientData


def get_word_for_lesson(username: str):
    db_words = ClientData()
    words = db_words.get_words(username)
    if len(words) != 0:
        db_words.delete_key(username, words[0][0])
        return words[0]
    db_all_words = AllWordsData()
    return db_all_words.get_word(int(random() * 499))
