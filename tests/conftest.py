import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base


def get_mock_session():
    engine = create_engine(
        settings.TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)

    test_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    session = test_session()
    yield session


class TestUser:

    def __init__(self):
        self.user_id = 1
        self.username = 'user1'
        self.password = 'supersecret'
        self.balance = 0
