from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    password_hash = Column(String(128))
    email = Column(String(255), unique=True, nullable=False)
    address = Column(String(255))
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_manager = Column(Boolean, default=False)
    gender_id = Column(Integer, ForeignKey('gender.id', ondelete='CASCADE'), nullable=False)
    appointment = db.relationship('Appointment', backref='user')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
