import os

from fastapi import status
from fastapi.testclient import TestClient

from config import settings
from database import get_session
from main import app
from tests.conftest import get_mock_session

client = TestClient(app)

app.dependency_overrides[get_session] = get_mock_session


def test_create_user():

    response1 = client.post(
        '/users/create',
        json={
            'username': 'user',
            'password': 'secret1',
        },
    )
    response2 = client.post(
        '/users/create',
        json={
            'username': 'user1',
            'password': 'secret1',
        },
    )
    response_409 = client.post(
        '/users/create',
        json={
            'username': 'user1',
            'password': 'secret3',
        },
    )

    os.remove(settings.TEST_DATABASE_PATH)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED
    assert response_409.status_code == status.HTTP_409_CONFLICT
