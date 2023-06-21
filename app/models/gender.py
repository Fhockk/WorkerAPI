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

    @classmethod
    def get_all_genders(cls):
        """
        Returns a list of all available genders.
        """
        genders = cls.query.all()
        return genders

    @classmethod
    def get_gender_by_name(cls, name):
        """
        Returns the gender object with the specified name.
        """
        gender = cls.query.filter_by(name=name).first()
        return gender
