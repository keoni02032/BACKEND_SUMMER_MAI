from datetime import datetime, timedelta

from pydantic import ValidationError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt

from .. import tables
from ..database import get_session
from sqlalchemy.orm import Session
from ..models.auth import Token, AdminCreate
from ..models.auth import Admin
from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_admin(token: str = Depends(oauth2_scheme)) -> Admin:
    return AuthService.validete_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hashed_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validete_token(cls, token: str) -> Admin:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError as e:
            raise exception from None

        admin_data = payload.get('admin')

        try:
            admin = Admin.parse_obj(admin_data)
        except ValidationError:
            raise exception from None

        return admin

    @classmethod
    def create_token(cls, admin: tables.Admin) -> Token:
        admin_data = Admin.from_orm(admin)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(admin_data.id),
            'admin': admin_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_admin(self, admin_data: AdminCreate) -> Token:
        admin = tables.Admin(
            email=admin_data.email,
            username=admin_data.username,
            password_hash=self.hashed_password(admin_data.password),
        )

        self.session.add(admin)
        self.session.commit()

        return self.create_token(admin)

    def authenticate_admin(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        admin = (
            self.session
            .query(tables.Admin)
            .filter(tables.Admin.username == username)
            .first()
        )

        if not admin:
            raise exception

        if not self.verify_password(password, admin.password_hash):
            raise exception

        return self.create_token(admin)
