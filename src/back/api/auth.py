from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import (
    Admin,
    AdminCreate,
    Token,
)
from ..services.auth import AuthService, get_current_admin

router = APIRouter(
    prefix='/auth',
)


@router.post('/sign-up', response_model=Token)
def sign_up(
    admin_data: AdminCreate,
    service: AuthService = Depends(),
):
    return service.register_new_admin(admin_data)


@router.post('/sign-in', response_model=Token)
def sign_uin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(),
):
    return service.authenticate_admin(
        form_data.username,
        form_data.password,
    )


@router.get('/user', response_model=Admin)
def get_admin(admin: Admin = Depends(get_current_admin)):
    return admin
