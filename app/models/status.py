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
