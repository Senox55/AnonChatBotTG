from dataclasses import dataclass, field
from environs import Env
from typing import Dict


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # Адрес базы данных
    db_port: str  # Порт базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class AgeConfig:
    age_ranges: dict[str, str] = field(default_factory=lambda: {
        17: 'до 17 лет',
        21: 'от 18 до 21 года',
        25: 'от 22 до 25 лет',
        35: 'от 26 до 35 лет',
        45: 'от 36 до 45 лет',
        46: 'старше 46',
    })


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    age: AgeConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_port=env('DB_PORT'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
        age=AgeConfig()
    )
