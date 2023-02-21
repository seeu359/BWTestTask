from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from models import schemes
from api.services import UserServices, get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post(
    path='/create',
    response_model=schemes.Token,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: schemes.CreateUser,
        user_services: UserServices = Depends()
) -> schemes.Token:

    return user_services.create_user(user_data)


@router.post(
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


@router.get(
    path='/balance',
    response_model=schemes.Balance,
    status_code=status.HTTP_200_OK,
)
async def get_user_balance(
        user: schemes.User = Depends(get_current_user),
        user_services: UserServices = Depends(UserServices),
):
    return user_services.get_user_balance(user.user_id)


@router.patch(
    path='/balance',
    status_code=status.HTTP_200_OK,
)
async def top_up_balance(
    user: schemes.User = Depends(get_current_user),
    user_service: UserServices = Depends(UserServices),
    body: dict = Body()
) -> schemes.Balance:

    return user_service.top_up_balance(user.user_id, body)


@router.post(
    path='/transfer',
    status_code=status.HTTP_200_OK,
    response_model=schemes.Transfer
)
async def money_transfer(
        user: schemes.User = Depends(get_current_user),
        user_service: UserServices = Depends(UserServices),
        body: dict = Body(),
) -> schemes.Transfer:

    return user_service.transfer(user.user_id, body)
