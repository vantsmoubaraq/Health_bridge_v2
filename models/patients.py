#!/usr/bin/python3

"""Module implements the patient class"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text, text
from os import getenv
from sqlalchemy.orm import relationship
import uuid

if models.storage_env == "db":
    patient_drug = Table("patients_drugs", Base.metadata,
                         Column("patient_id", String(60),
                                ForeignKey("patients.id", onupdate="CASCADE",
                                           ondelete="CASCADE"), primary_key=True),
                         Column("drug_id", String(60),
                                ForeignKey("drugs.id", onupdate="CASCADE",
                                           ondelete="CASCADE"), primary_key=True))


class Patient(BaseModel, Base):
    """Class Patient  describes the patient in the health facility"""
    if models.storage_env == "db":
        __tablename__ = "patients"
        name = Column(String(128), nullable=False)
        age = Column(Integer, nullable=True)
        gender = Column(String(60), nullable=False)
        address = Column(String(60), nullable=True)
        email = Column(String(128), nullable=True)
        clinical_notes = Column(Text, nullable=True)
        contact = Column(String(60), nullable=True)
        payments = relationship("Payment", backref="patient", cascade='all, delete')
        drugs = relationship("Drug", secondary="patients_drugs",
                             backref="patient_drugs", viewonly=False)

    if models.storage_env != "db":
        @property
        def drugs(self):
            """method returns all drugs prescribed for a patient"""
            from models.drugs import Drug
            drug_list = []
            for drug in models.storage.all(Drug).values():
                if drug.patient_id == self.id:
                    drug_list.append(drug)
            return drug_list

        @property
        def payments(self):
            """returns all payments against a patient"""
            from models.payments import Payment
            payment_list = []
            for payment in models.storage.all(Payment).values():
                if payment.patient_id == self.id:
                    payment_list.append(payment)
            return payment_list
