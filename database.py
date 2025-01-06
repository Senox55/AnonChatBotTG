import psycopg2
import psycopg2.extras
from config import user, host, password, db_name


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            port=5432,
            user=user,
            password=password,
            database=db_name,
        )
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    async def add_queue(self, chat_id: int, gender: str, desired_gender: str):
        query = "INSERT INTO queue (chat_id, gender, desired_gender) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (chat_id, gender, desired_gender))
        return True  # Возвращаем результат, если нужно

    async def delete_queue(self, chat_id):
        return self.cursor.execute(f"DELETE FROM queue WHERE chat_id = {chat_id}")

    async def delete_chat(self, id_chat):
        return self.cursor.execute(f"DELETE FROM chats WHERE id = {id_chat}")

    async def set_gender(self, chat_id, gender):
        self.cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
        user = self.cursor.fetchmany(1)
        if len(user) == 0:
            self.cursor.execute("INSERT INTO users (chat_id, gender) VALUES (%s, %s)", (chat_id, gender))
            self.connection.commit()
            return True
        else:
            return False

    async def update_gender(self, chat_id, gender):
        self.cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
        user = self.cursor.fetchmany(1)
        if len(user) != 0:
            self.cursor.execute('UPDATE users SET gender = %s WHERE chat_id = %s', (gender, chat_id))
            self.connection.commit()
            return True
        else:
            return False

    async def get_gender(self, chat_id):
        self.cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
        user = self.cursor.fetchmany(1)
        if len(user):
            for row in user:
                return row[2]
        else:
            return False

    async def get_chat(self, gender):
        if gender != 'anon':
            self.cursor.execute("SELECT * FROM queue WHERE gender = %s", (gender,))
            chat = self.cursor.fetchmany(1)
            if len(chat):
                for row in chat:
                    user_info = [row[0], row[2], row[3]]
                    return user_info
            else:
                return [0, 0, 0]
        else:
            self.cursor.execute("SELECT * FROM queue")
            chat = self.cursor.fetchmany(1)
            if len(chat):
                for row in chat:
                    user_info = [row[0], row[2], row[3]]
                    return user_info
            else:
                return [0, 0, 0]

    async def create_chat(self, chat_one, chat_two):
        if chat_two:
            # Создание чата
            await self.delete_queue(chat_two)
            self.cursor.execute("INSERT INTO chats (chat_one, chat_two)"
                                f"VALUES ({chat_one}, {chat_two})")
            return True
        else:
            # Становимся в очередь
            return False

    async def get_active_chat(self, chat_id):
        self.cursor.execute(f"SELECT * FROM chats WHERE chat_one = {chat_id}")
        chat = self.cursor.fetchall()
        id_chat = 0
        for row in chat:
            id_chat = row['id']
            chat_info = [row['id'], row['chat_two']]
        if id_chat == 0:
            self.cursor.execute(f"SELECT * FROM chats WHERE chat_two = {chat_id}")
            chat = self.cursor.fetchall()
            for row in chat:
                id_chat = row['id']
                chat_info = [row['id'], row['chat_one']]
            if id_chat == 0:
                return False
            else:
                return chat_info
        else:
            return chat_info

    async def increment_chat_count(self, user_id):
        self.cursor.execute('UPDATE users SET count_chat = count_chat + 1 WHERE chat_id = %s', (user_id,))
        self.connection.commit()

    async def is_in_queue(self, chat_id: int) -> bool:
        """
        Проверяет, находится ли пользователь в очереди.
        :param chat_id: ID чата пользователя
        :return: True, если пользователь в очереди, иначе False
        """
        query = "SELECT EXISTS(SELECT 1 FROM queue WHERE chat_id = %s)"
        self.cursor.execute(query, (chat_id,))
        result = self.cursor.fetchone()
        return result[0] == 1

    async def get_user_info(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE chat_id = %s', (user_id,))
        info = self.cursor.fetchone()
        if info:
            return info
        return False
