import enum
from sqlalchemy import Column, Integer, Enum

from app import db


class SpecialtyEnum(enum.Enum):
    SURGEON = 'Surgeon'
    ENT = 'Ent'
    OPHTHALMOLOGIST = 'Ophthalmologist'


class Specialty(db.Model):
    __tablename__ = 'specialty'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(SpecialtyEnum), nullable=False)
    worker = db.relationship('Worker', backref='specialty', uselist=False)
