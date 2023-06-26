#!/usr/bin/env python3

"""
Module implemenents users class
"""

from sqlalchemy import Column, Integer, String
from models.base_model import Base, BaseModel


class User(BaseModel, Base):
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