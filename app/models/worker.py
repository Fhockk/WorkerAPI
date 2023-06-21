from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class Worker(db.Model):
    __tablename__ = 'worker'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    gender_id = Column(Integer, ForeignKey('gender.id', ondelete='CASCADE'), nullable=False)
    specialty_id = Column(Integer, ForeignKey('specialty.id', ondelete='CASCADE'), nullable=False)
    schedule = db.relationship('Schedule', backref='worker')
    appointment = db.relationship('Appointment', backref='worker')

    def get_full_name(self):
        """
        Returns the full name of the worker.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def get_worker_by_email(self, email):
        """
        Returns the worker object with the specified email.
        """
        worker = Worker.query.filter_by(email=email).first()
        return worker
