from fastapi import Depends, HTTPException
from loguru import logger

from api import OperationStatuses
from database import Session, get_session
from models.orm_models import Operations as _Operations


class NotEnoughMoneyError(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code=status_code, detail=detail)


class Operations:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_operations(self, user_id: int, body: dict, exc=None) -> None:
        if exc is None:
            self.__add_operations(user_id,
                                  body,
                                  status=OperationStatuses.SUCCEEDED.value)
            return

        logger.info(
            f'Exc details - {exc.detail}, exc status code - {exc.status_code}'
        )
        self.__add_operations(user_id,
                              body,
                              status=OperationStatuses.FAILED.value)
        raise NotEnoughMoneyError(status_code=exc.status_code,
                                  detail=exc.detail)

    def __add_operations(self, user_id: int, body: dict, status: str):
        to_user_id = body.get('accountToId')
        operation = _Operations(
            from_user_id=user_id,
            to_user_id=to_user_id if to_user_id is not None else user_id,
            money_amount=body.get('amount'),
            status=status,
            type=body.get('type').upper(),
        )
        self.session.add(operation)
        self.session.commit()
        self.session.close()
