from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.authop import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, admin_id: int, review_id: int) -> tables.Feedback:
        review = (
            self.session
            .query(tables.Feedback)
            .filter_by(
                id=review_id,
                admin_id=admin_id,
            )
            .first()
        )
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return review

    def get_list(self, admin_id: int, id_user: int = None) -> List[tables.Feedback]:
        query = (
            self.session
            .query(tables.Feedback)
            .filter_by(admin_id=admin_id)
        )
        if id_user:
            query = query.filter_by(id_user=id_user)
        reviews = query.all()
        return reviews

    def get(self, admin_id: int, review_id: int) -> tables.Feedback:
        return self._get(admin_id, review_id)

    def create(self, review_data: ReviewCreate) -> tables.Feedback:
        review = tables.Feedback(**review_data.dict())
        self.session.add(review)
        self.session.commit()
        return review

    def update(self, admin_id: int, review_id: int, review_data: ReviewUpdate) -> tables.Feedback:
        review = self._get(admin_id, review_id)
        for field, value in review_data:
            setattr(review, field, value)
        self.session.commit()
        return review

    def delete(self, admin_id: int, review_id: int):
        review = self._get(admin_id, review_id)
        self.session.delete(review)
        self.session.commit()
