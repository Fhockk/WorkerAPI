import enum
from sqlalchemy import Column, Integer, Enum

from app import db


class GenderEnum(enum.Enum):
    MAN = 'Man'
    WOMAN = 'Woman'
    OTHER = 'Other'


class Gender(db.Model):
    __tablename__ = 'gender'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(GenderEnum), nullable=False)
    user = db.relationship('User', backref='gender', uselist=False)
    worker = db.relationship('Worker', backref='gender', uselist=False)
