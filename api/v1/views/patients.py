#!/usr/bin/python3

"""Module implements patients api"""

from flask import Flask, abort, jsonify, make_response, request
from models import storage, storage_env
from models.patients import Patient
from api.v1.views import ui
from models.base_model import BaseModel


@ui.route("/patients", methods=["GET", "POST"])
@ui.route("/patients/<string:patient_id>", methods=["GET", "PUT", "DELETE"])
def patients(patient_id=None):
    """Handles all default RESTful API actions for patient object"""
    if patient_id:
        patient = storage.get("Patient", patient_id)
        if not patient:
            abort(404)
            return

    if request.method == "GET":
        if patient_id:
            return jsonify(patient.to_dict())
        all_patients = [obj.to_dict() for obj in
                        storage.all("Patient").values()]
        return jsonify(all_patients)

    elif request.method == "POST":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        elif "name" not in request.get_json():
            return jsonify({"message": "name must be specified"})
        elif "gender" not in request.get_json():
            return jsonify({"message": "gender must be specified"})

        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"]  == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        obj = Patient(**attr)
        obj.save()
        pt = storage.get("Patient", obj.id)
        return make_response(jsonify(pt.to_dict()), 201)

    elif request.method == "PUT":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"] == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        for key, value in attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(patient, key, value)
        patient.save()
        pt = storage.get("Patient", patient.id)
        return make_response(jsonify(pt.to_dict()), 200)

    elif request.method == "DELETE":
        patient.delete()
        storage.save()
        return (jsonify({}))
