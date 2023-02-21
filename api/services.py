from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import orm_models, schemes
from database import get_session, Session
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> orm_models.User:
    return UserServices.verify_token(token)


class UserServices:

    @classmethod
    def verify_token(cls, token: str) -> orm_models.User:

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        try:
            payload = jwt.decode(
                token,
                key=settings.SECRET_KEY,
                algorithms=settings.algorithm,
            )
        except JWTError:
            raise exception

        user_data = payload.get('user')

        try:
            user = schemes.User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def is_valid_password(cls, password, password_hash):

        return bcrypt.verify(password, password_hash)

    @classmethod
    def get_hash_password(cls, password) -> str:

        return bcrypt.hash(password)

    @classmethod
    def create_jwt_token(cls, user_data: orm_models.User) -> schemes.Token:

        user = schemes.User.from_orm(user_data)
        time_now = datetime.utcnow()

        payload = {
            'exp': time_now + timedelta(hours=settings.expiration),
            'sub': str(user.user_id),
            'nbf': time_now,
            'iat': time_now,
            'user': user.dict(),
        }

        logger.info(payload)
        token = jwt.encode(
            payload,
            key=settings.SECRET_KEY,
            algorithm=settings.algorithm
        )

        return schemes.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def create_user(self, user_data: schemes.CreateUser) -> schemes.Token:
        user = orm_models.User(
            username=user_data.username,
            password=self.get_hash_password(user_data.password),
        )

        try:
            self.session.add(user)
            self.session.commit()

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Username already exists'
            )
        token = self.create_jwt_token(user)
        return token

    def authenticate_user(self, username: str, password: str) -> schemes.Token:

        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        user: orm_models.User = self.session.\
            query(orm_models.User).\
            filter(orm_models.User.username == username)\
            .first()

        if not user:
            raise exception

        if not self.is_valid_password(password, user.password):
            raise exception

        return self.create_jwt_token(user)

    def get_user_balance(self, user_id) -> schemes.Balance:
        user = self._get_user(user_id)
        balance = schemes.Balance(
            user_id=user.user_id,
            balance=user.balance,
        )
        return balance

    def top_up_balance(self, user_id, body) -> schemes.Balance:

        amount = body.get('amount')
        if amount is None or amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Amount cant be lower or equal zero'
            )
        user = self._get_user(user_id)
        user.balance += amount
        return schemes.Balance(user_id=user_id, balance=user.balance)

    def transfer(self, user_id, body) -> schemes.Transfer:
        transfer_user_id = body.get('accountToId')
        amount_transfer_money = body.get('amount')

        if transfer_user_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Incorrect transfer user id'
            )
        user = self._get_user(user_id)

        if amount_transfer_money > user.balance:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail='Not enough money for transfer'
            )

        user2 = self._get_user(transfer_user_id)
        if user2 is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User for transfer was not found',
            )
        user.balance -= amount_transfer_money
        user2.balance += amount_transfer_money

        return schemes.Transfer(
            author_id=user_id,
            credited_user_id=transfer_user_id,
            money_amount=amount_transfer_money,
        )

    def _get_user(self, user_id) -> orm_models.User:
        user = self.session.query(orm_models.User). \
            filter(orm_models.User.user_id == user_id).first()
        return user
