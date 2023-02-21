from pydantic import BaseModel


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


class Transfer(BaseModel):

    author_id: int
    credited_user_id: int | None = None
    money_amount: int
