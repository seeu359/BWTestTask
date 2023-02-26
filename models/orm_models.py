from datetime import datetime
from enum import Enum as _Enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column
from database import Base


class OperationStatus(_Enum):
    CREATED = 'CREATED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class OperationType(_Enum):
    PAYIN = 'PAYIN'
    TRANSFER = 'TRANSFER'
    PAYOUT = 'PAYOUT'


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    balance = Column(Integer, default=0)


class Operations(Base):
    __tablename__ = 'operation'

    operation_id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = mapped_column(ForeignKey('user.user_id'))
    to_user_id = mapped_column(ForeignKey('user.user_id'))
    status = Column(Enum(OperationStatus))
    type = Column(Enum(OperationType))
    money_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
