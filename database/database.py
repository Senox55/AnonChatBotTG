from typing import Any, Union

import asyncpg
from datetime import datetime, timedelta


class Database():
    def __init__(self, connection: asyncpg.Pool):
        self.connection = connection

    async def add_queue(self, user_id: int):
        """
        Функция для добавления пользователя в очередь поиска
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            INSERT 
              INTO queue (user_id) 
            VALUES ($1)
            """,
            user_id
        )

    async def delete_queue(self, user_id: int):
        """
        Функция для удаления пользователя из очереди поиска
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            DELETE 
              FROM queue 
             WHERE user_id = $1
            """,
            user_id
        )

    async def delete_chat(self, chat_id: int):
        """
        Функция удаления чата по его id
        :param chat_id:
        :return:
        """
        await self.connection.execute(
            """
            DELETE 
              FROM chats 
             WHERE id = $1
            """,
            chat_id
        )

    async def set_gender(self, user_id, gender) -> bool:
        """
        Функция для установки гендера пользователя, если его еще нет
        :param user_id:
        :param gender:
        :return:
        """
        user = await self.connection.fetchval(
            """
            SELECT 1
              FROM users 
             WHERE id = $1
             """,
            user_id
        )

        if not user:
            await self.connection.execute(
                """INSERT 
                     INTO users (id, gender) 
                   VALUES ($1, $2)
                   """,
                user_id, gender
            )
            return True
        return False

    async def update_gender(self, user_id: int, gender: str) -> bool:
        """
        Функция для обновления пола пользователя, при его наличии
        :param user_id:
        :param gender:
        :return:
        """
        user = await self.connection.fetchval(
            """
            SELECT 1
              FROM users 
             WHERE id = $1
             """,
            user_id
        )

        if user:
            await self.connection.execute(
                """
                UPDATE users 
                   SET gender = $1 
                 WHERE id = $2
                 """,
                gender, user_id
            )
            return True
        return False

    async def get_gender(self, user_id: int) -> Union[bool, str]:
        """
        Функция получения пола пользователя по его id
        :param user_id:
        :return:
        """
        user_gender = await self.connection.fetchval(
            """
            SELECT gender
              FROM users 
             WHERE id = $1
             """,
            user_id
        )

        return user_gender if user_gender else False

    async def get_age(self, user_id: int) -> Union[bool, int]:
        """
        Функция получения возраста пользователя по его id
        :param user_id:
        :return:
        """
        user_age = await self.connection.fetchval(
            """
            SELECT age
              FROM users 
             WHERE id = $1
            """,
            user_id
        )

        return user_age if user_age else False

    async def set_age(self, user_id: int, age: int) -> bool:
        """
        Функция установки пола пользователя по id, при его существования
        :param user_id:
        :param age:
        :return:
        """
        user = await self.connection.fetchrow(
            """
            SELECT 1 
              FROM users 
             WHERE id = $1
             """,
            user_id
        )

        if user:
            await self.connection.execute(
                """
                UPDATE users 
                   SET age = $1 
                 WHERE id = $2
                    """,
                age, user_id
            )
            return True
        return False

    async def set_preferred_gender(self, user_id: int, preferred_gender: str):
        """
        Функция установки желаемого пола собеседника по id пользователя
        :param user_id:
        :param preferred_gender:
        :return:
        """
        await self.connection.fetchrow(
            """
            UPDATE users 
               SET preferred_gender = $1 
             WHERE id = $2
            """,
            preferred_gender,
            user_id
        )

    async def get_preferred_gender(self, user_id: int) -> str:
        """
        Получение желаемого пола собеседника по id пользователя
        :param user_id:
        :return:
        """
        preferred_gender = await self.connection.fetchval(
            """
            SELECT preferred_gender
            FROM users
            WHERE id = $1
            """,
            user_id
        )
        return preferred_gender

    async def get_chat(self, gender: str, preferred_gender: str) -> Union[int, bool]:
        """
        Функция получения первого подходящего пользователя из очереди
        :param gender:
        :param preferred_gender:
        :return:
        """
        if preferred_gender:
            chat_id = await self.connection.fetchval(
                """
                SELECT u.id
                  FROM queue AS q
                  JOIN users AS u
                    ON q.user_id = u.id
                 WHERE u.gender = $1 AND (u.preferred_gender = $2 OR u.preferred_gender IS NULL)
                   """,
                preferred_gender, gender
            )
        else:

            chat_id = await self.connection.fetchval(
                """
                SELECT u.id
                  FROM queue AS q
                  JOIN users AS u
                    ON q.user_id = u.id
                 WHERE (u.preferred_gender = $1 OR u.preferred_gender IS NULL)
                """,
                gender
            )

        return chat_id if chat_id else False

    async def create_chat(self, user_id_one: int, user_id_two: int) -> bool:
        """
        Функция для создания общего чата 2 пользователей по их id, при их наличии
        :param user_id_one:
        :param user_id_two:
        :return:
        """
        if user_id_two:
            # Создание чата
            await self.delete_queue(user_id_two)
            await self.connection.execute(
                """
                    INSERT 
                      INTO chats (user_id_one, user_id_two)
                    VALUES ($1, $2)
                    """,
                user_id_one, user_id_two
            )
            return True
        # Становимся в очередь
        return False

    async def get_active_chat(self, user_id_one: int) -> Union[(bool, [int, int])]:
        """
        Функция для получения id активного чата и id собеседника при их наличии
        :param user_id_one:
        :return:
        """
        chat = await self.connection.fetchrow(
            """
            SELECT id, user_id_two 
              FROM chats 
             WHERE user_id_one = $1
            """,
            user_id_one
        )

        if not chat:
            chat = await self.connection.fetchrow(
                """
                SELECT id, user_id_one as user_id_two 
                  FROM chats 
                 WHERE user_id_two = $1
                 """,
                user_id_one
            )

        if chat:
            return [chat['id'], chat['user_id_two']]
        return False

    async def increment_chat_count(self, user_id: int):
        """
        Функция для подсчёта проведенных чатов пользователя по id
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            UPDATE users 
               SET count_chats = count_chats + 1 
             WHERE id = $1
             """,
            user_id
        )

    async def is_in_queue(self, user_id: int) -> bool:
        """
        Функция для проверки, находится ли пользователь в очереди
        :param user_id:
        :return:
        """

        exists = await self.connection.fetchval(
            """
            SELECT EXISTS(SELECT 1 
                            FROM queue 
                           WHERE user_id = $1)
            """,
            user_id
        )
        return exists

    async def get_user_info(self, user_id: int):
        """
        Функция для получения полной информации о пользователе по id при его наличии
        :param user_id:
        :return:
        """
        info = await self.connection.fetchrow(
            """
            SELECT * 
              FROM users 
             WHERE id = $1
             """,
            user_id
        )
        return info if info else False

    async def get_vip_status(self, user_id: int) -> Union[list, bool]:
        """
        Функция для получения полной информации о вип статусе по id пользователя, при его наличии
        :param user_id:
        :return:
        """
        info = await self.connection.fetchrow(
            """
            SELECT *
              FROM vip_statuses
             WHERE user_id = $1
             """,
            user_id
        )
        return info if info else False

    async def give_vip(self, user_id: int, duration: int):
        """
        Функция для выдачи или продления вип статуса по id пользователя
        :param user_id:
        :param duration:
        :return:
        """
        vip_status = await self.get_vip_status(user_id)

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
                INSERT 
                  INTO vip_statuses (user_id, duration, start_date, end_date)
                VALUES ($1, $2, $3, $4)
                """,
                user_id, duration, start_date, end_date
            )

    async def deactivate_vip_status(self, user_id: int):
        """
        Функция для деактивации вип по id пользователя
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            DELETE
              FROM vip_statuses
             WHERE user_id = $1
            """,
            user_id
        )

    async def is_alive(self, user_id: int) -> bool:
        """
        Функция для проверки, заблокировал ли пользователь бота
        :param user_id:
        :return:
        """
        is_alive = await self.connection.fetchval(
            """
            SELECT is_alive
              FROM users
             WHERE id = $1
            """,
            user_id
        )
        return is_alive

    async def set_alive_to_false(self, user_id: int):
        """
        Функция для установки пользователя в неактивные, если он заблокировал бота
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            UPDATE users
               SET is_alive = False
             WHERE id = $1
            """,
            user_id
        )

    async def set_alive_to_true(self, user_id: int):
        """
        Функция для установки пользователя в активные, если он разблокировал бота
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            UPDATE users
               SET is_alive = True
             WHERE id = $1
            """,
            user_id
        )

    async def get_user_state(self, user_id: int):
        """
        Функция для получения состояния пользователя по id
        :param user_id:
        :return:
        """
        state_info = await self.connection.fetchrow(
            """
            SELECT state, data
              FROM user_states
             WHERE user_id = $1
            """,
            user_id
        )
        return state_info

    async def clear_user_state(self, user_id: int):
        """
        Функция для очистки всех состояний пользователя по id
        :param user_id:
        :return:
        """
        await self.connection.execute(
            """
            DELETE
              FROM user_states
             WHERE user_id = $1
            """,
            user_id
        )

    async def set_user_state(self, user_id: int, state: str, data='{}'):
        """
        Функция для установки состояния пользователя по id
        :param user_id:
        :param state:
        :param data:
        :return:
        """
        user_info = await self.connection.fetchval(
            """
            SELECT 1 
              FROM user_states 
             WHERE user_id = $1
            """,
            user_id
        )
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
                INSERT 
                  INTO user_states (user_id, state, data) 
                VALUES ($1, $2, $3)
                """,
                user_id,
                state,
                data
            )

    async def send_report(self, reported_user_id: int, reporter_user_id: int, reason: str):
        """
        Функция для записи репорта, если он до этого не был отправлен
        :param reported_user_id:
        :param reporter_user_id:
        :param reason:
        :return:
        """
        report_info = await self.connection.fetchval(
            """
            SELECT 1
              FROM reports
             WHERE reported_user_id = $1 AND reporter_user_id = $2
            """,
            reported_user_id, reporter_user_id
        )

        if not report_info:
            await self.connection.execute(
                """
                INSERT 
                  INTO reports (reported_user_id, reporter_user_id, reason) 
                VALUES ($1, $2, $3)
                """,
                reported_user_id,
                reporter_user_id,
                reason
            )

    async def change_user_chat_mode(self, user_id: int, safe_mode: bool):
        """
        Функция для смены режима безопасности чата по id пользователя
        :param user_id:
        :param safe_mode:
        :return:
        """
        await self.connection.execute(
            """
            UPDATE users
               SET safe_mode = $1
             WHERE id = $2
            """,
            safe_mode, user_id
        )

    async def get_user_chat_mode(self, user_id: int):
        """
        Функция для получения режима безопасности чата по id пользователя
        :param user_id:
        :return:
        """
        is_save = await self.connection.fetchval(
            """
            SELECT safe_mode
              FROM users
             WHERE id = $1
            """,
            user_id
        )
        return is_save
