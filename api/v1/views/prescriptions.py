#!/usr/bin/env python3

"""
Module implements all prescriptions restful API routes
"""

from flask import Flask, request, abort, jsonify
from models import storage
from models.prescriptions import Prescription
from api.v1.views import ui

@ui.route('/prescriptions/<string:patient_id>', methods=["POST"])
@ui.route('/prescription/<string:prescription_id>', methods=["GET", "DELETE"])
def prescriptions(patient_id=None, prescription_id=None):
    """Methods handles all restful api operations"""
    if not patient_id and not prescription_id:
        return jsonify({"message": "error"})
    if request.method == "POST":
        patient = storage.get("Patient", patient_id)
        if not patient:
            return jsonify({"message": "error"})
        obj = Prescription(patient_id=patient_id)
        obj.save()
        storage.save()
        return jsonify(obj.to_dict()), 200
    elif request.method == "GET":
        prescription = storage.get("Prescription", prescription_id)
        if not prescription:
            return jsonify({"message": "invalid prescription id"})
        return jsonify(prescription.to_dict()), 200
    elif request.method == "DELETE":
        prescription = storage.get("Prescription", prescription_id)
        storage.delete(prescription)
        return jsonify("{}")