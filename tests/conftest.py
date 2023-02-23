import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base

engine = create_engine(
        settings.TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )


@pytest.fixture()
def db_service():
    Base.metadata.create_all(engine)


def get_mock_session():

    test_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    session = test_session()
    yield session


class TestUser:

    def __init__(self):
        username = 'user1'
        password = 'supersecret'