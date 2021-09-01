from pydantic import BaseModel


class BaseAdmin(BaseModel):
    email: str
    username: str


class AdminCreate(BaseAdmin):
    password: str


class Admin(BaseAdmin):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
