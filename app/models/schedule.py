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

    def get_duration_minutes(self):
        """
        Calculates and returns the duration of the schedule in minutes.
        """
        start = self.start_time
        end = self.end_time
        duration = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        return duration

    @classmethod
    def get_schedules_by_worker(cls, worker_id):
        """
        Retrieves all schedules associated with a specific worker ID.
        """
        schedules = cls.query.filter_by(worker_id=worker_id).all()
        return schedules
