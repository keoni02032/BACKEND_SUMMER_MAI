from typing import List
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.operations import OperationCreate, OperationUpdate


class OperationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, operation_id: int) -> tables.Operation:
        operation = (
            self.session
            .query(tables.Operation)
            .filter_by(id=operation_id)
            .first()
        )
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, group_name: Optional[str] = None) -> List[tables.Operation]:
        query = self.session.query(tables.Operation)
        if group_name:
            query = query.filter_by(group_name=group_name)
        operations = query.all()
        return operations

    def get(self, operation_id: int) -> tables.Operation:
        return self._get(operation_id)

    def create(self, admin_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(
            **operation_data.dict(),
            admin_id=admin_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, admin_id: int, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        if admin_id:
            operation = self._get(operation_id)
            for field, value in operation_data:
                setattr(operation, field, value)
            self.session.commit()
            return operation

    def delete(self, admin_id: int, operation_id: int):
        if admin_id:
            operation = self._get(operation_id)
            self.session.delete(operation)
            self.session.commit()
