from fastapi import Depends, HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from api.services.auth import JWTToken
from database import Session, get_session
from models import orm_models, schemes


def get_user(session, user_id: int) -> orm_models.User:
    user = session.query(orm_models.User). \
        filter(orm_models.User.user_id == user_id).first()
    return user


class UserServicesMixin:

    @classmethod
    def is_valid_password(cls, password, password_hash):
        return bcrypt.verify(password, password_hash)

    @classmethod
    def get_hash_password(cls, password) -> str:
        return bcrypt.hash(password)


class UserServices(UserServicesMixin):

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
        token = JWTToken.create_jwt_token(user)
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

        if not user or not self.is_valid_password(password, user.password):
            raise exception

        return JWTToken.create_jwt_token(user)
