#!/usr/bin/python3

"""Module handles all api actions for patients_drugs relationship"""

from flask import Flask, jsonify, request, make_response, abort
from models.patients import Patient
from models.drugs import Drug
from models import storage
from models import storage_env
from api.v1.views import ui


@ui.route("/patient/<string:patient_id>/drug", methods=["GET"])
@ui.route("/patient/<string:patient_id>/drug/<string:drug_id>", methods=["POST", "DELETE"])
def patient_drug(patient_id, drug_id=None):
    """Handles all default api actions for patients_drugs relationship"""
    if patient_id is None:
        return
    
    patient = storage.get("Patient", patient_id)
    if patient is None:
        abort(404)
        return

    if drug_id:
        drug = storage.get("Drug", drug_id)
        if drug is None:
            abort(404)
            return

    patient = storage.get("Patient", patient_id)

    patient_drugs = patient.drugs

    if request.method == "GET":
        return jsonify([drug.to_dict() for drug in patient_drugs])

    elif request.method == "POST":
        if drug in patient_drugs:
            drug.quantity -= 1
            patient_drugs.append(drug)
            drug.save()
            patient.save()
            drug = storage.get("Drug", drug_id)
            return jsonify(drug.to_dict())
        patient_drugs.append(drug)
        drug.quantity -= 1
        drug.save()
        patient.save()
        drug = storage.get("Drug", drug_id)
        return jsonify(drug.to_dict())

    elif request.method == "DELETE":
        patient_drugs.remove(drug)
        storage.save()
        return jsonify({})

