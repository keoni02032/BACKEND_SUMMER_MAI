from typing import List

from fastapi import APIRouter
from fastapi import Depends

from ..models.authop import Review, ReviewCreate, ReviewUpdate
from ..services.auth import get_current_admin
from ..services.authop import ReviewService
from fastapi import Response
from fastapi import status

from ..tables import Admin

router = APIRouter(
    prefix='/authop',
)


@router.get('/', response_model=List[Review])
def get_feedback(
    id_user: int = None,
    admin: Admin = Depends(get_current_admin),
    service: ReviewService = Depends(),
):
    return service.get_list(admin_id=admin.id, id_user=id_user)


@router.post('/', response_model=Review)
def create_feedback(
    review_data: ReviewCreate,
    service: ReviewService = Depends(),
):
    return service.create(review_data)


@router.get('/{review_id}', response_model=Review)
def get_feedback(
    review_id: int,
    admin: Admin = Depends(get_current_admin),
    service: ReviewService = Depends(),
):
    return service.get(admin_id=admin.id, review_id=review_id)


@router.put('/{review_id}', response_model=Review)
def update_feedback(
    review_id: int,
    review_data: ReviewUpdate,
    admin: Admin = Depends(get_current_admin),
    service: ReviewService = Depends(),
):
    return service.update(
        admin_id=admin.id,
        review_id=review_id,
        review_data=review_data,
    )


@router.delete('/{review_id}')
def delete_feedback(
    review_id: int,
    admin: Admin = Depends(get_current_admin),
    service: ReviewService = Depends(),
):
    service.delete(admin_id=admin.id, review_id=review_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)