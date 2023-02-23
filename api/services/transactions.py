from fastapi import Depends, HTTPException, status

from api import get_user
from database import Session, get_session
from models import schemes


class BaseTransactions:

    def get_balance(self, user_id) -> schemes.Balance:
        user = get_user(self.session, user_id)
        return schemes.Balance(
            user_id=user.user_id,
            balance=user.balance,
        )

    @staticmethod
    def check_money_amount(balance: int, payout_amount: int):
        if balance < payout_amount:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail='Insufficient funds'
            )


class Transactions(BaseTransactions):

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def pay_in(self, user_id, body) -> schemes.Balance:
        data = schemes.PayIn(**body)
        user = get_user(self.session, user_id)
        user.balance += data.amount
        return schemes.Balance(user_id=user_id, balance=user.balance)

    def pay_out(self, user_id: int, body: dict) -> schemes.Balance:
        data = schemes.PayOut(**body)
        user = get_user(self.session, user_id)
        self.check_money_amount(user.balance, data.amount)
        user.balance -= data.amount
        return schemes.Balance(user_id=user_id, balance=user.balance)

    def transfer(self, user_id, body) -> schemes.Transfer:
        data = schemes.Transfer(**body)
        user = get_user(self.session, user_id)
        self.check_money_amount(user.balance, data.amount)

        user2 = get_user(self.session, data.accountToId)
        if user2 is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User for transfer was not found',
            )

        user.balance -= data.amount
        user2.balance += data.amount

        return schemes.Transfer(
            author_id=user_id,
            accountToId=data.accountToId,
            amount=data.amount,
            type='transfer',
        )
