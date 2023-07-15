#!/usr/bin/python3

"""Module implements the Payment  class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
import models


class Payment(BaseModel, Base):
    """Class Payment describes the the bills against patients"""
    if models.storage_env == "db":
        __tablename__ = "payments"
        patient_id = Column(String(60), ForeignKey("patients.id"),
                            nullable=False)
        paid = Column(Integer, nullable=True)
        invoice_id = Column(String(60), ForeignKey("invoices.id", ondelete="CASCADE"))
        invoice = relationship("Invoice", back_populates="payments")