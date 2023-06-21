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
