#!/usr/bin/python3

"""
Module implements invoice functionality
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.drugs import Drug


class Invoice(BaseModel, Base):
    """Implements invoice schema"""
    __tablename__ = "invoices"
    patient_id = Column(String(60), ForeignKey("patients.id"))
    prescription_id = Column(String(60), ForeignKey("prescriptions.id"), nullable=True)
    prescription = relationship("Prescription", backref="prescriptions")
    patient = relationship("Patient", back_populates="invoices", overlaps="invoices")
    invoiced_services = relationship("Invoiced_services")
    payments = relationship("Payment", back_populates="invoice")