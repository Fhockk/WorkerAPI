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

    def get_date_parts(self):
        """
        Returns the year, month, and day of the appointment's day attribute.
        """
        year = self.day.year
        month = self.day.month
        day = self.day.day
        return year, month, day

    def get_duration(self):
        """
        Returns the duration of the appointment in minutes.
        """
        start = self.start_time
        end = self.end_time
        duration = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        return duration
