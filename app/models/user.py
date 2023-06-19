from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    address = Column(String(255))
    gender_id = Column(Integer, ForeignKey('gender.id', ondelete='CASCADE'), nullable=False)
    appointment = db.relationship('Appointment', backref='user')
