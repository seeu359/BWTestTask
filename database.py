import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

load_dotenv()

if os.getenv('CI') is None:
    DATABASE_URL = f'postgresql+psycopg2://{settings.POSTGRES_USER}:' \
                   f'{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:' \
                   f'{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
else:
    DATABASE_URL = settings.TEST_DATABASE_URL

Base = declarative_base()


engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_session():
    session = Session()
    try:
        yield session
    except: # noqa E722
        session.rollback()
    else:
        session.commit()
    finally:
        session.close()
