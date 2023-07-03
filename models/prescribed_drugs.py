#!/usr/bin/env python3

"""Module implements prescribed drugs"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Prescribed_drug(BaseModel, Base):
    """Class creates schema for prescribed drug"""
    __tablename__ = "prescribed_drugs"
    drug_id = Column(String(60), ForeignKey("drugs.id"))
    prescription_id = Column(String(60), ForeignKey("prescriptions.id"))
    dosage = Column(Integer, nullable=True)
    frequency = Column(Integer, nullable=False)
    doctor = Column(String(128), nullable=True)
    days = Column(Integer, nullable=False)
    drug = relationship("Drug", backref="prescribed_drugs")