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

    @classmethod
    def get_all_locations(cls):
        """
        Returns a list of all available locations.
        """
        locations = cls.query.all()
        return locations

    @classmethod
    def get_location_by_place(cls, place):
        """
        Returns the location object with the specified place.
        """
        location = cls.query.filter_by(place=place).first()
        return location
