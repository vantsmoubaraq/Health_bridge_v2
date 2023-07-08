#!/usr/bin/env python3

"""Module implements prescriptions table"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from models.prescribed_drugs import Prescribed_drug


class Prescription(BaseModel, Base):
    """Class implements prescription"""
    __tablename__ = "prescriptions"
    patient_id = Column(String(60), ForeignKey("patients.id"))
    prescribed_drugs = relationship("Prescribed_drug")
    patient = relationship("Patient", back_populates="prescriptions", overlaps="prescriptions")
    

"""
    # Event listener function
def update_drug_quantity_after_insert(mapper, connection, target):
    # Get the related Drug instance
    print("Event Triggered")
    drug = target.drug
    print(drug)
    if drug is not None:
        # Calculate the quantity to update
        quantity_update = target.days * target.frequency
        print(f'quantity_update: {quantity_update}')
        # Update the quantity column in the Drug table
        drug.quantity -= quantity_update
        print(f'New quantity: {drug.quantity}')
        connection.execute(
            Drug.__table__.update().values(quantity=drug.quantity).where(Drug.id == drug.id)
        )

# Register the event listener
event.listen(Prescription, 'after_insert', update_drug_quantity_after_insert)
"""