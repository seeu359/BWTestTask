from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from pydantic import ValidationError

from config import settings
from models import orm_models, schemes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> orm_models.User:
    return JWTToken.verify_token(token)


class JWTToken:

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
