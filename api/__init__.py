from enum import Enum

from api.services.auth import get_current_user
from api.services.users import get_user


class OperationStatuses(Enum):
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


__all__ = (
    'get_user',
    'get_current_user',
    'OperationStatuses',
)
