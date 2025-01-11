import asyncpg


class Database():
    def __init__(self, connection: asyncpg.Pool):
        self.connection = connection

    async def add_queue(self, user_id: int, gender: str, desired_gender: str):
        await self.connection.execute("INSERT INTO queue (user_id, gender, desired_gender) VALUES ($1, $2, $3)",
                                      user_id, gender, desired_gender)

        return True  # Возвращаем результат, если нужно

    async def delete_queue(self, user_id):
        status = await self.connection.execute("DELETE FROM queue WHERE user_id = $1",
                                               user_id)

        return status.split()[-1]  # Возвращает количество удалённых строк

    async def delete_chat(self, chat_id):
        status = await self.connection.execute("DELETE FROM chats WHERE id = %s",
                                               chat_id)
        return status.split()[-1]  # Возвращает количество удалённых строк

    async def set_gender(self, user_id, gender):
        user = await self.connection.fetch(f"SELECT * FROM users WHERE user_id = $1", user_id)
        if not user:
            await self.connection.execute("INSERT INTO users (user_id, gender) VALUES ($1, $2)", user_id, gender)
            return True
        else:
            return False

    async def update_gender(self, user_id, gender):
        user = await self.connection.fetch(f"SELECT * FROM users WHERE user_id = $1", user_id)
        if user:
            await self.connection.execute('UPDATE users SET gender = $1 WHERE user_id = $2', gender, user_id)
            return True
        else:
            return False

    async def get_gender(self, user_id):
        user = await self.connection.fetchrow(f"SELECT * FROM users WHERE user_id = $1", user_id)
        return user['gender'] if user else False

    async def get_chat(self, gender):
        if gender != 'anon':
            chat = await self.connection.fetchrow("SELECT * FROM queue WHERE gender = $1", gender)
        else:
            chat = await self.connection.fetchrow(
                "SELECT user_id, gender, desired_gender FROM queue"
            )

        if chat:
            return [chat['user_id'], chat['gender'], chat['desired_gender']]
        return [0, 0, 0]

    async def create_chat(self, user_id_one, user_id_two):
        if user_id_two:
            # Создание чата
            await self.delete_queue(user_id_two)
            await self.connection.execute("INSERT INTO chats (user_id_one, user_id_two)"
                                          f"VALUES ($1, $2)", user_id_one, user_id_two)
            return True
        # Становимся в очередь
        return False

    async def get_active_chat(self, user_id_one):
        chat = await self.connection.fetchrow(
            "SELECT id, user_id_two FROM chats WHERE user_id_one = $1",
            user_id_one
        )
        if not chat:
            chat = await self.connection.fetchrow(
                "SELECT id, user_id_one as user_id_two FROM chats WHERE user_id_two = $1",
                user_id_one
            )

        if chat:
            return [chat['id'], chat['user_id_two']]
        return False

    async def increment_chat_count(self, user_id):
        exists = await self.connection.execute('UPDATE users SET count_chats = count_chats + 1 WHERE user_id = $1',
                                               user_id)
        return exists

    async def is_in_queue(self, user_id: int) -> bool:
        """
        Проверяет, находится ли пользователь в очереди.
        :param chat_id: ID чата пользователя
        :return: True, если пользователь в очереди, иначе False
        """

        exists = await self.connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM queue WHERE user_id = $1)",
            user_id
        )
        return exists

    async def get_user_info(self, user_id):
        info = await self.connection.fetchrow(
            'SELECT * FROM users WHERE user_id = $1',
            user_id
        )
        return info if info else False
