from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api import get_current_user
from api.services.operations import Operations
from api.services.transactions import Transactions
from api.services.users import UserServices
from models import schemes

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
        transactions: Transactions = Depends(Transactions),
):
    return transactions.get_balance(user.user_id)


@router.patch(
    path='/balance/payin',
    status_code=status.HTTP_200_OK,
)
async def pay_in(
    user: schemes.User = Depends(get_current_user),
    transactions: Transactions = Depends(Transactions),
    operations: Operations = Depends(Operations),
    body: dict = Body(),
):
    """Request body must include fields:
    amount: int = <amount of money to payin>,
    type: str = payin
    """
    balance = transactions.pay_in(user.user_id, body)
    operations.add_operations(user.user_id, body)
    return balance


@router.post(
    path='/transfer',
    status_code=status.HTTP_200_OK,
    response_model=schemes.Transfer
)
async def transfer(
    user: schemes.User = Depends(get_current_user),
    transactions: Transactions = Depends(Transactions),
    operations: Operations = Depends(Operations),
    body: dict = Body(),
) -> schemes.Transfer:
    """Request body must include fields:
        accountToId: int = <recipient id>,
        amount: int = <amount of money to payin>
        type: str = transfer
        """
    try:
        _transfer = transactions.transfer(user.user_id, body)
        operations.add_operations(user.user_id, body)
        return _transfer

    except HTTPException as exc:
        operations.add_operations(user.user_id, body, exc=exc)


@router.post(
    path='/balance/payout',
    status_code=status.HTTP_200_OK,
    response_model=schemes.Balance,
)
def pay_out(
    user: schemes.User = Depends(get_current_user),
    transactions: Transactions = Depends(Transactions),
    operations: Operations = Depends(Operations),
    body: dict = Body(),
) -> schemes.Balance:
    """Request body must include fields:
        amount: int = <amount of money to payin>,
        type: str = payout
    """
    try:
        balance = transactions.pay_out(user.user_id, body)
        operations.add_operations(user.user_id, body)
        return balance

    except HTTPException as exc:
        operations.add_operations(user.user_id, body, exc=exc)
