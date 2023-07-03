#!/usr/bin/env python3

"""Module implements all restful api operations"""

from flask import request, jsonify, abort
from models import storage
from models.prescribed_drugs import Prescribed_drug
from api.v1.views import ui


@ui.route("/prescribe_drug/<string:prescription_id>", methods=["POST"])
@ui.route("/prescribed_drug/<string:prescribed_drug_id>", methods=["GET", "PUT", "DELETE"])
def prescribe_drug(prescription_id=None, prescribed_drug_id=None):
    """Method implements all restful api operations"""
    if prescription_id is None and prescribed_drug_id is None:
        abort(400)
    elif prescription_id:
        prescription = storage.get("Prescription", prescription_id)
        if not prescription:
            return jsonify({"message": "invalid prescription_id"})
        patient_id = prescription.patient_id
    elif prescribed_drug_id:
        prescribed_drug = storage.get("Prescribed_drug", prescribed_drug_id)
        if not prescribed_drug:
            return jsonify({"message": "invalid prescribed_drug_id"})
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return
        elif "drug_id" not in data:
            return jsonify({"message": "drug missing"})
        elif "frequency" not in data:
            return jsonify({"message": "frequecy of intake missing"})
        elif "days" not in data:
            return jsonify({"message": "days missing"})
        else:
            data["prescription_id"] = prescription_id
            new_prescribed_drug = Prescribed_drug(**data)
            new_prescribed_drug.save()
            return jsonify(new_prescribed_drug.to_dict()), 200
    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return
        for key, value in data.values():
            if key not in ["prescription_id", "id", "created_at", "updated_at"]:
                setattr(prescribed_drug, key, value)
        prescribed_drug.save()
        return jsonify(prescribed_drug), 201
    elif request.method == "GET":
        return jsonify(prescribed_drug.to_dict()), 200
    elif request.method == "DELETE":
        storage.delete(prescribed_drug)
        return jsonify({})
