#!/usr/bin/python3

"""Module implements the drug class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class Drug(BaseModel, Base):
    """Class Drug provides a description of the medicine"""
    if models.storage_env == "db":
        __tablename__ = "drugs"
        name = Column(String(128), nullable=False)
        quantity = Column(Integer, nullable=False, default=0)
        price = Column(Integer, nullable=True)
