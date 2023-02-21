import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    SECRET_KEY: str
    algorithm: str = 'HS256'
    expiration: int = 24
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DATABASE_URL: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
