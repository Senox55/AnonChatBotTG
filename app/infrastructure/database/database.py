import logging
from typing import Any, Union

import asyncpg
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Database():
    def __init__(self, connection: asyncpg.Pool):
        self.connection = connection

    #
    # async def get_gender(self, user_id: int) -> Union[bool, str]:
    #     """
    #     Функция получения пола пользователя по его id
    #     :param user_id:
    #     :return:
    #     """
    #     user_gender = await self.connection.fetchval(
    #         """
    #         SELECT gender
    #           FROM users
    #          WHERE id = $1
    #          """,
    #         user_id
    #     )
    #
    #     return user_gender if user_gender else False
    #
    # async def get_age(self, user_id: int) -> Union[bool, int]:
    #     """
    #     Функция получения возраста пользователя по его id
    #     :param user_id:
    #     :return:
    #     """
    #     user_age = await self.connection.fetchval(
    #         """
    #         SELECT age
    #           FROM users
    #          WHERE id = $1
    #         """,
    #         user_id
    #     )
    #
    #     return user_age if user_age else False
    #
    #
    # async def set_preferred_gender(self, user_id: int, preferred_gender: str):
    #     """
    #     Функция установки желаемого пола собеседника по id пользователя
    #     :param user_id:
    #     :param preferred_gender:
    #     :return:
    #     """
    #     await self.connection.fetchrow(
    #         """
    #         UPDATE users
    #            SET preferred_gender = $1
    #          WHERE id = $2
    #         """,
    #         preferred_gender,
    #         user_id
    #     )
    #
    # async def get_preferred_gender(self, user_id: int) -> str:
    #     """
    #     Получение желаемого пола собеседника по id пользователя
    #     :param user_id:
    #     :return:
    #     """
    #     preferred_gender = await self.connection.fetchval(
    #         """
    #         SELECT preferred_gender
    #         FROM users
    #         WHERE id = $1
    #         """,
    #         user_id
    #     )
    #     return preferred_gender

    # async def increment_chat_count(self, user_id: int):
    #     """
    #     Функция для подсчёта проведенных чатов пользователя по id
    #     :param user_id:
    #     :return:
    #     """
    #     await self.connection.execute(
    #         """
    #         UPDATE users
    #            SET count_chats = count_chats + 1
    #          WHERE id = $1
    #          """,
    #         user_id
    #     )
    #
    #
    #
    # async def get_vip_status(self, user_id: int) -> Union[list, bool]:
    #     """
    #     Функция для получения полной информации о вип статусе по id пользователя, при его наличии
    #     :param user_id:
    #     :return:
    #     """
    #     info = await self.connection.fetchrow(
    #         """
    #         SELECT *
    #           FROM vip_statuses
    #          WHERE user_id = $1
    #          """,
    #         user_id
    #     )
    #     return info if info else False
    #
    # async def give_vip(self, user_id: int, duration: int):
    #     """
    #     Функция для выдачи или продления вип статуса по id пользователя
    #     :param user_id:
    #     :param duration:
    #     :return:
    #     """
    #     vip_status = await self.get_vip_status(user_id)
    #
    #     if vip_status:
    #         # Если у пользователя уже есть активный VIP-статус, продлеваем его
    #         await self.connection.execute(
    #             """
    #             UPDATE vip_statuses
    #                SET end_date = end_date + make_interval(days => $1)
    #              WHERE user_id = $2
    #             """,
    #             duration,  # Передаём строку вида '30 days'
    #             user_id
    #         )
    #     else:
    #         # Если активного VIP-статуса нет, создаём новый
    #         start_date = datetime.now()
    #         end_date = start_date + timedelta(days=duration)
    #
    #         # Создаём новую запись в таблице vip_statuses
    #         await self.connection.execute(
    #             """
    #             INSERT
    #               INTO vip_statuses (user_id, duration, start_date, end_date)
    #             VALUES ($1, $2, $3, $4)
    #             """,
    #             user_id, duration, start_date, end_date
    #         )
    #
    # async def deactivate_vip_status(self, user_id: int):
    #     """
    #     Функция для деактивации вип по id пользователя
    #     :param user_id:
    #     :return:
    #     """
    #     await self.connection.execute(
    #         """
    #         DELETE
    #           FROM vip_statuses
    #          WHERE user_id = $1
    #         """,
    #         user_id
    #     )
    #
    # async def is_alive(self, user_id: int) -> bool:
    #     """
    #     Функция для проверки, заблокировал ли пользователь бота
    #     :param user_id:
    #     :return:
    #     """
    #     is_alive = await self.connection.fetchval(
    #         """
    #         SELECT is_alive
    #           FROM users
    #          WHERE id = $1
    #         """,
    #         user_id
    #     )
    #     return is_alive

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

    async def get_users_info(self):
        users_info = await self.connection.fetch(
            """
            SELECT *
              FROM users
            """
        )
        return users_info

    async def create_users_with_parameters_view(self):
        """
        Создает или обновляет представление users_with_parameters
        для всех пользователей с их параметрами
        """
        try:
            await self.connection.execute(
                """
                CREATE OR REPLACE VIEW public.users_with_parameters AS
                SELECT 
                        u.id AS user_id, 
                        u.telegram_id,
                        up.id AS parameter_id,
                        p.name AS parameter_name,
                        up.value AS parameter_value,
                        p.description AS description,
                        up.data_type AS parameter_value_data
                  FROM users u
                  JOIN users_parameters up ON up.user_id = u.id
                  JOIN parameters p ON up.parameter_id = p.id
                """
            )
            logger.info("View users_with_parameters создано успешно")
        except Exception as e:
            logger.warning(f"Ошибка при создании view: {e}")

    async def get_user_info(self, user_id: int):
        """
        Получает информацию о конкретном пользователе из представления

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            dict: Информация о пользователе
        """
        try:
            # Сначала убеждаемся, что представление существует
            await self.create_users_with_parameters_view()

            # Получаем информацию о пользователе
            user_info = await self.connection.fetch(
                """
                SELECT * FROM public.users_with_parameters
                WHERE telegram_id = $1
                """,
                str(user_id)
            )

            return user_info
        except Exception as e:
            logger.warning(f"Ошибка при получении информации о пользователе: {e}")
            return []

    async def add_user(self, user_id: int, gender: int, age: int):
        await self.connection.execute(
            """
            call create_user_proc(uuid_generate_v4(), $1, $2, $3);
            """,
            str(user_id), str(gender), age

        )

    async def update_user_parameter(self, user_id: int, parameter_name: str, new_value: str) -> bool:
        """
        Обновляет параметр пользователя в таблице users_parameters.

        Args:
            user_id (int): Идентификатор пользователя (telegram_id)
            parameter_name (str): Имя параметра, который нужно обновить
            new_value (str): Новое значение параметра

        Returns:
            bool: Успешность операции
        """
        try:
            # Обновляем параметр в таблице users_parameters
            await self.connection.execute(
                """
                UPDATE users_parameters
                SET value = $1
                WHERE user_id = (
                    SELECT id FROM users WHERE telegram_id = $2
                ) 
                AND parameter_id = (
                    SELECT id FROM parameters WHERE name = $3
                )
                """,
                new_value,
                str(user_id),
                parameter_name
            )
            logger.info(
                f"Параметр '{parameter_name}' пользователя с Telegram ID {user_id} успешно обновлен до {new_value}.")
            return True
        except Exception as e:
            logger.warning(
                f"Ошибка при обновлении параметра '{parameter_name}' пользователя с Telegram ID {user_id}: {e}")
            return False

    async def update_age(self, user_id: int, new_age: int) -> bool:
        """
        Обновляет возраст пользователя.

        Args:
            user_id (int): Идентификатор пользователя
            new_age (int): Новый возраст пользователя

        Returns:
            bool: Успешность операции
        """
        return await self.update_user_parameter(user_id, 'age', str(new_age))

    async def update_gender(self, user_id: int, new_gender: str) -> bool:
        """
        Обновляет пол пользователя.

        Args:
            user_id (int): Идентификатор пользователя
            new_gender (str): Новый пол пользователя

        Returns:
            bool: Успешность операции
        """
        return await self.update_user_parameter(user_id, 'gender', new_gender)

    async def update_preferred_room_capacity(self, user_id: int, new_capacity: int) -> bool:
        """
        Обновляет предпочтительную вместимость комнаты пользователя.

        Args:
            user_id (int): Идентификатор пользователя
            new_capacity (int): Новая вместимость комнаты

        Returns:
            bool: Успешность операции
        """
        return await self.update_user_parameter(user_id, 'preferred_room_capacity', str(new_capacity))

    async def update_chat_mode(self, user_id: int, new_mode: bool) -> bool:
        """
        Обновляет режим чата пользователя (безопасный режим).

        Args:
            user_id (int): Идентификатор пользователя
            new_mode (bool): Новый режим чата

        Returns:
            bool: Успешность операции
        """
        return await self.update_user_parameter(user_id, 'safe_mode', str(new_mode))

    async def update_alive(self, user_id: int, is_alive: bool) -> bool:

        return await self.update_user_parameter(user_id, 'is_alive', str(is_alive))

    async def update_preferred_gender(self, user_id: int, preferred_gender: str) -> bool:
        """
        Обновляет предпочтительную вместимость комнаты пользователя.

        Args:
            user_id (int): Идентификатор пользователя
            new_capacity (int): Новая вместимость комнаты

        Returns:
            bool: Успешность операции
        """
        return await self.update_user_parameter(user_id, 'preferred_gender', str(preferred_gender))