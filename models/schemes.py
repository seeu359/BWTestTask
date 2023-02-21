from typing import Literal

from pydantic import BaseModel, Field


class BaseUser(BaseModel):

    username: str


class User(BaseUser):

    user_id: int

    class Config:

        orm_mode = True


class CreateUser(BaseUser):

    password: str


class Token(BaseModel):

    access_token: str
    token_type: str = 'bearer'


class Balance(BaseModel):

    user_id: int
    balance: float


class Operations(BaseModel):
    amount: int | float = Field(None, gt=0)


class PayIn(Operations):
    type: Literal['payin']


class PayOut(Operations):
    type: Literal['payout']


class Transfer(Operations):
    author_id: int | None
    accountToId: int
    type: Literal['transfer']
