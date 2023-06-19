from sqlalchemy import Column, Integer, Date, Time, ForeignKey

from app import db


class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    worker_id = Column(Integer, ForeignKey('worker.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id', ondelete='CASCADE'), default=1)
