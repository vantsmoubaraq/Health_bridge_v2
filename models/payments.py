#!/usr/bin/python3

"""Module implements the Payment  class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from os import getenv
import models


class Payment(BaseModel, Base):
    """Class Payment describes the the bills against patients"""
    if models.storage_env == "db":
        __tablename__ = "payments"
        patient_id = Column(String(60), ForeignKey("patients.id"),
                            nullable=False)
        amount = Column(Integer, nullable=False)
        paid = Column(Integer, nullable=True)
