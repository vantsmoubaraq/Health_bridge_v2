#!/usr/bin/env python3

"""
Module implemenents users class
"""

from sqlalchemy import Column, Integer, String
from models.base_model import Base, BaseModel
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(BaseModel, Base, UserMixin):
    """Class implements User"""
    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    contact = Column(String(60), nullable=True)
    role = Column(String(128), nullable=True)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Login Required Methods

    def is_authenticated(self):
        return True  # Assuming all users are authenticated

    def is_active(self):
        return True  # Assuming all users are active

    def is_anonymous(self):
        return False  # Assuming all users are not anonymous

    def get_id(self):
        return str(self.id)  # Convert the user ID to string
