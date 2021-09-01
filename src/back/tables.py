import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admin'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Text, unique=True)
    email = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.String, nullable=True)
    text = sa.Column(sa.String)
    date = sa.Column(sa.Date)
    rating = sa.Column(sa.Integer)
    admin_id = sa.Column(sa.Integer, sa.ForeignKey('admin.id'))


class Operation(Base):
    __tablename__ = 'operations'

    id = sa.Column(sa.Integer, primary_key=True)
    group_name = sa.Column(sa.String, nullable=True)
    type = sa.Column(sa.String, nullable=True)
    start = sa.Column(sa.String)
    stop = sa.Column(sa.String)
    date = sa.Column(sa.Date)
    date_editing = sa.Column(sa.Date)
    admin_id = sa.Column(sa.Integer, sa.ForeignKey('admin.id'))
