from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    address = Column(String(255))
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    gender_id = Column(Integer, ForeignKey('gender.id', ondelete='CASCADE'), nullable=False)
    appointment = db.relationship('Appointment', backref='user')
