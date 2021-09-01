from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from ..models.operations import Operation, OperationCreate, OperationUpdate
from ..services.auth import get_current_admin
from ..services.operations import OperationService
from ..tables import Admin

router = APIRouter(
    prefix='/operations',
)


@router.get('/', response_model=List[Operation])
def get_operations(
    group_name: Optional[str] = None,
    service: OperationService = Depends(),
):
    return service.get_list(group_name=group_name)


@router.post('/', response_model=Operation)
def create_operation(
    operation_data: OperationCreate,
    admin: Admin = Depends(get_current_admin),
    service: OperationService = Depends(),
):
    return service.create(admin_id=admin.id, operation_data=operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(
    operation_id: int,
    service: OperationService = Depends(),
):
    return service.get(operation_id)



@router.put('/{operation_id}', response_model=Operation)
def update_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    admin: Admin = Depends(get_current_admin),
    service: OperationService = Depends(),
):
    return service.update(
        admin_id=admin.id,
        operation_id=operation_id,
        operation_data=operation_data,
    )


@router.delete('/{operation_id}')
def delete_operation(
    operation_id: int,
    admin: Admin = Depends(get_current_admin),
    service: OperationService = Depends(),
):
    service.delete(admin_id=admin.id, operation_id=operation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
