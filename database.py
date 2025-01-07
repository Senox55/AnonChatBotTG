import psycopg2
import psycopg2.extras
import os


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('HOST'),
            port=5432,
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DB_NAME'),
        )
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    async def add_queue(self, user_id: int, gender: str, desired_gender: str):
        query = "INSERT INTO queue (user_id, gender, desired_gender) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user_id, gender, desired_gender))
        return True  # Возвращаем результат, если нужно

    async def delete_queue(self, user_id):
        return self.cursor.execute(f"DELETE FROM queue WHERE user_id = {user_id}")

    async def delete_chat(self, chat_id):
        return self.cursor.execute(f"DELETE FROM chats WHERE id = {chat_id}")

    async def set_gender(self, user_id, gender):
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user = self.cursor.fetchmany(1)
        if len(user) == 0:
            self.cursor.execute("INSERT INTO users (user_id, gender) VALUES (%s, %s)", (user_id, gender))
            self.connection.commit()
            return True
        else:
            return False

    async def update_gender(self, user_id, gender):
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user = self.cursor.fetchmany(1)
        if len(user) != 0:
            self.cursor.execute('UPDATE users SET gender = %s WHERE user_id = %s', (gender, user_id))
            self.connection.commit()
            return True
        else:
            return False

    async def get_gender(self, user_id):
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
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

    async def create_chat(self, user_id_one, user_id_two):
        if user_id_two:
            # Создание чата
            await self.delete_queue(user_id_two)
            self.cursor.execute("INSERT INTO chats (user_id_one, user_id_two)"
                                f"VALUES ({user_id_one}, {user_id_two})")
            return True
        else:
            # Становимся в очередь
            return False

    async def get_active_chat(self, user_id_one):
        self.cursor.execute(f"SELECT * FROM chats WHERE user_id_one = {user_id_one}")
        chat = self.cursor.fetchall()
        id_chat = 0
        for row in chat:
            id_chat = row['id']
            chat_info = [row['id'], row['user_id_two']]
        if id_chat == 0:
            self.cursor.execute(f"SELECT * FROM chats WHERE user_id_two = {user_id_one}")
            chat = self.cursor.fetchall()
            for row in chat:
                id_chat = row['id']
                chat_info = [row['id'], row['user_id_one']]
            if id_chat == 0:
                return False
            else:
                return chat_info
        else:
            return chat_info

    async def increment_chat_count(self, user_id):
        self.cursor.execute('UPDATE users SET count_chats = count_chats + 1 WHERE user_id = %s', (user_id,))
        self.connection.commit()

    async def is_in_queue(self, user_id: int) -> bool:
        """
        Проверяет, находится ли пользователь в очереди.
        :param chat_id: ID чата пользователя
        :return: True, если пользователь в очереди, иначе False
        """
        query = "SELECT EXISTS(SELECT 1 FROM queue WHERE user_id = %s)"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] == 1

    async def get_user_info(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        info = self.cursor.fetchone()
        if info:
            return info
        return False
