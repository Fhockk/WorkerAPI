import enum
from sqlalchemy import Column, Integer, Enum

from app import db


class LocationEnum(enum.Enum):
    HOSPITAL_ROOM_6 = 'Hospital room №6'
    HOSPITAL_ROOM_7 = 'Hospital room №7'
    DUTY = 'On duty'


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    place = Column(Enum(LocationEnum), nullable=False)
    schedule = db.relationship('Schedule', backref='location')
