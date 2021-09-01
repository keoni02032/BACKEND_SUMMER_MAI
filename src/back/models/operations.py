from datetime import date
from typing import Optional

from pydantic import BaseModel


class OperationBase(BaseModel):
    group_name: Optional[str]
    type: Optional[str]
    # start: Optional[str]
    # stop: Optional[str]
    date: date
    # date_editing: date
    # admin_id: int

class Operation(OperationBase):
    id: int

    class Config:
        orm_mode = True


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass
