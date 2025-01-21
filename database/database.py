import asyncpg
from datetime import datetime, timedelta


class Database():
    def __init__(self, connection: asyncpg.Pool):
        self.connection = connection

    async def add_queue(self, user_id: int):
        await self.connection.execute("INSERT INTO queue (user_id) VALUES ($1)",
                                      user_id)

    async def delete_queue(self, user_id):
        await self.connection.execute("DELETE FROM queue WHERE user_id = $1",
                                      user_id)

    async def delete_chat(self, chat_id):
        await self.connection.execute("DELETE FROM chats WHERE id = $1",
                                      chat_id)

    async def set_gender(self, user_id, gender):
        user = await self.connection.fetch(f"SELECT * FROM users WHERE id = $1", user_id)
        if not user:
            await self.connection.execute("INSERT INTO users (id, gender) VALUES ($1, $2)", user_id, gender)
            return True
        else:
            return False

    async def update_gender(self, user_id, gender):
        user = await self.connection.fetch(f"SELECT * FROM users WHERE id = $1", user_id)
        if user:
            await self.connection.execute('UPDATE users SET gender = $1 WHERE id = $2', gender, user_id)
            return True
        else:
            return False

    async def get_gender(self, user_id):
        user = await self.connection.fetchrow(f"SELECT * FROM users WHERE id = $1", user_id)
        return user['gender'] if user else False

    async def get_age(self, user_id):
        user = await self.connection.fetchrow(f"SELECT * FROM users WHERE id = $1", user_id)
        return user['age'] if user else False

    async def set_age(self, user_id, age):
        user = await self.connection.fetch(f"SELECT * FROM users WHERE id = $1", user_id)
        if user:
            await self.connection.execute("UPDATE users SET age = $1 WHERE id = $2", age, user_id)
            return True
        else:
            return False

    async def set_preferred_gender(self, user_id, preferred_gender):
        await self.connection.fetchrow(
            """
            UPDATE users SET preferred_gender = $1 WHERE id = $2
            """,
            preferred_gender,
            user_id
        )

    async def get_preferred_gender(self, user_id):
        await self.connection.fetchrow(
            """
            SELECT preferred_gender
            FROM users
            WHERE id = $1
            """,
            user_id
        )

    async def get_chat(self, gender, preferred_gender):
        if preferred_gender:
            chat = await self.connection.fetchrow(
                """SELECT u.id
                    FROM queue AS q
                    JOIN users AS u
                        ON q.user_id = u.id
                    WHERE u.gender = $1 AND (u.preferred_gender = $2 OR u.preferred_gender IS NULL)""",
                preferred_gender, gender)
        else:

            chat = await self.connection.fetchrow(
                """SELECT u.id
                FROM queue AS q
                JOIN users AS u
                    ON q.user_id = u.id
                WHERE (u.preferred_gender = $1 OR u.preferred_gender IS NULL)""",
                gender
            )

        if chat:
            return chat['id']
        return False

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
        exists = await self.connection.execute('UPDATE users SET count_chats = count_chats + 1 WHERE id = $1',
                                               user_id)
        return exists

    async def is_in_queue(self, user_id: int) -> bool:

        exists = await self.connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM queue WHERE user_id = $1)",
            user_id
        )
        return exists

    async def get_user_info(self, user_id):
        info = await self.connection.fetchrow(
            'SELECT * FROM users WHERE id = $1',
            user_id
        )
        return info if info else False

    async def check_vip_status(self, user_id):
        info = await self.connection.fetchrow(
            """SELECT vip_id FROM users WHERE user_id = $1""",
            user_id
        )
        return info['vip_id']

    async def get_vip_status(self, user_id):
        info = await self.connection.fetchrow(
            """SELECT *
            FROM vip_statuses as u
            WHERE u.user_id = $1""",
            user_id
        )
        if info:
            return info
        return False

    async def give_vip(self, user_id: int, duration: int):
        vip_status = self.get_vip_status(user_id)

        if vip_status:
            # Если у пользователя уже есть активный VIP-статус, продлеваем его
            await self.connection.execute(
                """
                UPDATE vip_statuses
                SET end_date = end_date + make_interval(days => $1)
                WHERE user_id = $2
                """,
                duration,  # Передаём строку вида '30 days'
                user_id
            )
        else:
            # Если активного VIP-статуса нет, создаём новый
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration)

            # Создаём новую запись в таблице vip_statuses
            await self.connection.execute(
                """
                INSERT INTO vip_statuses (user_id, duration, start_date, end_date)
                VALUES ($1, $2, $3, $4)
                RETURNING id
                """,
                user_id, duration, start_date, end_date
            )

    async def deactivate_vip_status(self, user_id):
        await self.connection.execute(
            """
            DELETE
            FROM vip_statuses
            WHERE user_id = $1
            """,
            user_id
        )

    async def is_alive(self, user_id):
        is_alive = await self.connection.fetchrow(
            """
            SELECT is_alive
            FROM users
            WHERE id = $1
            """,
            user_id
        )
        return is_alive["is_alive"]

    async def set_alive_to_false(self, user_id):
        await self.connection.execute(
            """
            UPDATE users
            set is_alive = False
            WHERE id = $1
            """,
            user_id
        )

    async def set_alive_to_true(self, user_id):
        await self.connection.execute(
            """
            UPDATE users
            set is_alive = True
            WHERE id = $1
            """,
            user_id
        )

    async def get_user_state(self, user_id):
        state_info = await self.connection.fetchrow(
            """
            SELECT state, data
            FROM user_states
            WHERE user_id = $1
            """,
            user_id
        )
        return state_info

    async def clear_user_state(self, user_id):
        await self.connection.execute(
            """
            DELETE
            FROM user_states
            WHERE user_id = $1
            """,
            user_id
        )

    async def set_user_state(self, user_id, state, data='{}'):
        user_info = await self.connection.fetchrow(
            """
            SELECT 1 FROM user_states WHERE user_id = $1
            """,
            user_id)
        if user_info:
            await self.connection.execute(
                """
                UPDATE user_states
                SET state = $1, data = $2
                WHERE user_id = $3
                """,
                state,
                data,
                user_id
            )
        else:
            await self.connection.execute(
                """
                INSERT INTO user_states (user_id, state, data) VALUES ($1, $2, $3)
                """,
                user_id,
                state,
                data
            )
