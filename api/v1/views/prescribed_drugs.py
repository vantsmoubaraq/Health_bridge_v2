#!/usr/bin/env python3

"""Module implements all restful api operations"""

from flask import request, jsonify, abort
from models import storage
from models.prescribed_drugs import Prescribed_drug
from api.v1.views import ui
from werkzeug.datastructures import MultiDict


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
        drug = storage.get("Drug", prescribed_drug.drug_id)
    
    if request.method == "POST":
        if "drug_id" not in request.form:
            return jsonify({"message": "drug missing"})
        elif "frequency" not in request.form:
            return jsonify({"message": "frequecy of intake missing"})
        elif "days" not in request.form:
            return jsonify({"message": "days missing"})
        else:
            new_form_data = MultiDict(request.form)
            new_form_data["prescription_id"] = prescription_id
            new_prescribed_drug = Prescribed_drug(**new_form_data)
            drug = storage.get("Drug", new_form_data["drug_id"])
            days = int(new_form_data["days"])
            frequency = int(new_form_data["frequency"])
            drug.quantity -= (frequency * days)
            new_prescribed_drug.save()
            return jsonify(new_prescribed_drug.to_dict()), 200
    elif request.method == "PUT":
        data = request.form
        if not data:
            return
        if data["drug_id"] != prescribed_drug.drug_id:
            drug.quantity  += int(prescribed_drug.frequency) * int(prescribed_drug.days)
            drug.save()
            new_drug = storage.get("Drug", data["drug_id"])
            new_drug.quantity -= int(data["frequency"]) * int(data["days"])
            new_drug.save()
        else:
            quantity = int(data["frequency"]) * int(data["days"])
            addition = (int(prescribed_drug.frequency) * int(prescribed_drug.days)) - quantity
            drug.quantity += addition
        """
        elif "frequency" in data.keys():
            quantity = int(data["frequency"]) * int(prescribed_drug.days)
            addition = (int(prescribed_drug.frequency) * int(prescribed_drug.days)) - quantity
            drug.quantity += addition
        elif "days" in data.keys():
            quantity = int(prescribed_drug.frequency) * int(data["days"])
            addition = (int(prescribed_drug.frequency) * int(prescribed_drug.days)) - quantity
            drug.quantity += addition"""

        for key, value in data.items():
            if key not in ["prescription_id", "id", "created_at", "updated_at"]:
                setattr(prescribed_drug, key, value)
        prescribed_drug.save()
        return jsonify(prescribed_drug.to_dict()), 201
    elif request.method == "GET":
        return jsonify(prescribed_drug.to_dict()), 200
    elif request.method == "DELETE":
        drug.quantity += (int(prescribed_drug.frequency) * int(prescribed_drug.days))
        drug.save()
        storage.delete(prescribed_drug)
        return jsonify({})
