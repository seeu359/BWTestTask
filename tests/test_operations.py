import os

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api import get_current_user
from config import settings
from database import get_session
from main import app
from tests.conftest import TestUser, get_mock_session

client = TestClient(app)


def test_payin_operations():
    app.dependency_overrides[get_session] = get_mock_session
    app.dependency_overrides[get_current_user] = TestUser

    client.post(
        'users/create',
        json={
            'username': 'user1',
            'password': 'secret1',
        },
    )

    response = client.patch(
        'users/balance/payin',
        json={"amount": 50, "type": "payin"}
    )

    os.remove(settings.TEST_DATABASE_PATH)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('payout_money, status_code',
                         [
                             (30, status.HTTP_200_OK),
                             (50, status.HTTP_200_OK),
                             (70, status.HTTP_402_PAYMENT_REQUIRED),
                         ])
def test_payout_operations(payout_money, status_code):
    app.dependency_overrides[get_session] = get_mock_session
    app.dependency_overrides[get_current_user] = TestUser

    client.post(
        'users/create',
        json={
            'username': 'user1',
            'password': 'secret1',
        },
    )

    response_payin = client.patch(
        'users/balance/payin',
        json={"amount": 50, "type": "payin"}
    )
    response_payout = client.post(
        'users/balance/payout',
        json={"amount": payout_money, "type": "payout"}
    )

    os.remove(settings.TEST_DATABASE_PATH)
    assert response_payin.status_code == status.HTTP_200_OK
    assert response_payout.status_code == status_code


@pytest.mark.parametrize('first_transfer, second_transfer, status_code1, status_code2',
                         [
                             (20, 80, status.HTTP_200_OK, status.HTTP_200_OK),
                             (30, 50, status.HTTP_200_OK, status.HTTP_200_OK),
                             (30, 71, status.HTTP_200_OK, status.HTTP_402_PAYMENT_REQUIRED),
                             (40, 60, status.HTTP_200_OK, status.HTTP_200_OK),
                             (101, 60, status.HTTP_402_PAYMENT_REQUIRED, status.HTTP_200_OK),
                         ])
def test_transfer_operations(first_transfer, second_transfer, status_code1, status_code2):
    app.dependency_overrides[get_session] = get_mock_session
    app.dependency_overrides[get_current_user] = TestUser

    client.post(
        'users/create',
        json={
            'username': 'user1',
            'password': 'secret1',
        },
    )
    client.post(
        'users/create',
        json={
            'username': 'user2',
            'password': 'secret1',
        },
    )

    response_payin = client.patch(
        'users/balance/payin',
        json={"amount": 100, "type": "payin"}
    )
    transfer1 = client.post(
        'users/transfer',
        json={"amount": first_transfer, "type": "transfer", "accountToId": 2}
    )
    transfer2 = client.post(
        'users/transfer',
        json={"amount": second_transfer, "type": "transfer", "accountToId": 2}
    )
    os.remove(settings.TEST_DATABASE_PATH)
    assert response_payin.status_code == status.HTTP_200_OK
    assert transfer1.status_code == status_code1
    assert transfer2.status_code == status_code2
