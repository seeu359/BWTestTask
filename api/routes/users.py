from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.services.users import UserServices
from models import schemes

users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@users_router.post(
    path='/create',
    response_model=schemes.Token,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: schemes.CreateUser,
        user_services: UserServices = Depends()
) -> schemes.Token:

    return user_services.create_user(user_data)


@users_router.post(
    path='/login',
    response_model=schemes.Token,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServices = Depends(),
) -> schemes.Token:

    return user_service.authenticate_user(
        form_data.username,
        form_data.password,
    )
