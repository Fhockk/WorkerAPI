import enum
from sqlalchemy import Column, Integer, Enum

from app import db


class StatusEnum(enum.Enum):
    AWAITING = 'Awaiting'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'
    MISSED = 'Missed'


class Status(db.Model):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(StatusEnum), nullable=False)
    appointment = db.relationship('Appointment', backref='status', uselist=False)

    @classmethod
    def get_all_statuses(cls):
        """
        Returns a list of all available statuses.
        """
        statuses = cls.query.all()
        return statuses

    @classmethod
    def get_status_by_name(cls, name):
        """
        Returns the status object with the specified name.
        """
        status = cls.query.filter_by(name=name).first()
        return status
