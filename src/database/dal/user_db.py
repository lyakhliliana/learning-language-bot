import sqlite3
from typing import List


class ClientData:
    path = "database/data/client_data"

    def __init__(self):
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS client (                    
            username   TEXT,                    
            first_word TEXT,
            second_word TEXT          
             )""")
        connection.commit()

    def get_words(self, username: str):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT first_word, second_word FROM client WHERE client.username = '{username}';""")
        res: List = cursor.fetchall()
        return res

    def insert_key(self, username: str, first: str, second: str):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM client WHERE client.username = '{username}' AND client.first_word = '{first}';")
        connection.commit()

        cursor.execute("INSERT INTO client(username, first_word, second_word) VALUES(?, ?, ?)",
                       (username, first, second))
        connection.commit()

    def delete_key(self, username: str, first: str):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM client WHERE client.username = '{username}' AND client.first_word = '{first}';")
        connection.commit()
