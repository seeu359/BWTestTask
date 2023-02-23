import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings

load_dotenv()

LOGGER_FORMAT = '{time:YYYY.MM.DD - HH:mm:ss} - {level} - {message}'


class Settings(BaseSettings):

    SECRET_KEY: str
    BASE_DIR: Path = Path(__file__).resolve().parent
    PATH_TO_LOGS = BASE_DIR / 'api' / 'logs' / 'logs.log'
    LOGGER_FORMAT: str = '{time:YYYY.MM.DD - HH:mm:ss} - {level} - {message}'
    algorithm: str = 'HS256'
    expiration: int = 24
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str = 'sqlite:///' + os.path.join(
        str(BASE_DIR) + '/tests/test_db.sqlite3'
    )
    TEST_DATABASE_PATH: str = os.path.join(
        str(BASE_DIR) + '/tests/test_db.sqlite3'
    )


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

LOGGER = logger.add(
    sink=settings.PATH_TO_LOGS,
    level='INFO',
    format=settings.LOGGER_FORMAT,
)
