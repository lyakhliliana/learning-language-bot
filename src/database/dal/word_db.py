import sqlite3
from typing import List


class AllWordsData:
    path = "database/data/all_words"

    def get_word(self, id: int):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT russian_translation, english_word
            FROM common_english_words WHERE common_english_words.id = {id};""")
        res: List = cursor.fetchall()
        return res[0]
