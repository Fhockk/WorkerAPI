from datetime import time
from sqlalchemy import Column, Integer, Date, Time, ForeignKey, UniqueConstraint

from app import db


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False, default=time(8, 0))
    end_time = Column(Time, nullable=False, default=time(17, 0))
    worker_id = Column(Integer, ForeignKey('worker.id', ondelete='CASCADE'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('day', 'worker_id'),)
