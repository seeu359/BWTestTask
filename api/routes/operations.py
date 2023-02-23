from fastapi import APIRouter, Body, Depends, HTTPException, status

from api import get_current_user
from api.services.operations import Operations
from api.services.transactions import Transactions
from models import schemes

operations_router = APIRouter(
    prefix='/users',
    tags=['Operations']
)


@operations_router.get(
    path='/balance',
    response_model=schemes.Balance,
    status_code=status.HTTP_200_OK,
)
async def get_user_balance(
        user: schemes.User = Depends(get_current_user),
        transactions: Transactions = Depends(Transactions),
):
    return transactions.get_balance(user.user_id)


@operations_router.patch(
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


@operations_router.post(
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


@operations_router.post(
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
