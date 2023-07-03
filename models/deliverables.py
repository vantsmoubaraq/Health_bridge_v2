#!/usr/bin/env python3

"""Module implements deliverables against invoice"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Deliverable(BaseModel, Base):
    """class implements schema deliverables"""
    __tablename__ = "deliverables"
    patient_id = Column(String(60), ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="deliverables", overlaps="deliverables")
