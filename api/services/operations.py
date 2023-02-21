from fastapi import Depends
from database import Session, get_session
from models.orm_models import Operations as _Operations


class Operations:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_operations(self, user_id: int, body: dict, status: str):
        to_user_id = body.get('accountToId')
        operation = _Operations(
            from_user_id=user_id,
            to_user_id=to_user_id if to_user_id is not None else user_id,
            money_amount=body.get('amount'),
            status=status,
            type=body.get('type').upper(),
        )
        self.session.add(operation)
