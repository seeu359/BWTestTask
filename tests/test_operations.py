import os

from fastapi import status
from fastapi.testclient import TestClient

from api import get_current_user
from config import settings
from database import get_session
from main import app
from tests.conftest import TestUser, get_mock_session

client = TestClient(app)

app.dependency_overrides[get_session] = get_mock_session


def test_pay_in(db_service):
    app.dependency_overrides[get_current_user] = TestUser

    response = client.patch(
        'users/balance/payin',
        data={'amount': 50, 'type': 'payin'}
    )

    os.remove(settings.TEST_DATABASE_PATH)
    assert response.status_code == status.HTTP_200_OK
