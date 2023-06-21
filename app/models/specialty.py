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

    @classmethod
    def get_all_specialties(cls):
        """
        Returns a list of all available specialties.
        """
        specialties = cls.query.all()
        return specialties

    @classmethod
    def get_specialty_by_name(cls, name):
        """
        Returns the specialty object with the specified name.
        """
        specialty = cls.query.filter_by(name=name).first()
        return specialty
