from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReviewBase(BaseModel):
    user: Optional[str]
    text: Optional[str]
    date: date
    rating: int


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass