#!/usr/bin/python3

"""Module handles all default RESTful API actions Drug class"""

from flask import Flask, render_template, jsonify, make_response, request, abort
from models import storage
from models.drugs import Drug
from api.v1.views import ui


@ui.route("/pharmacy", methods=["GET", "POST"])
@ui.route("/pharmacy/<string:drug_id>", methods=["GET", "PUT", "DELETE"])
def pharmacy(drug_id=None):
    """Handles all default RESTful API actions for Drug class"""
    if drug_id:
        drug = storage.get("Drug", drug_id)
        if drug is None:
            abort(404)
            return

    if request.method == "GET":
        if drug_id is None:
            all_drugs = [drug.to_dict() for drug in
                         storage.all("Drug").values()]
            return jsonify(all_drugs)
        return jsonify(drug)

    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid json"})
        elif "name" not in data:
            return jsonify({"message": "Drug name must be specified"})
        elif "quantity" not in data:
            return jsonify({"message": "Drug quantity must be specified"})
        if data["price"] == "None" or data["price"] == "" or data["price"] == None:
            del data["price"]
        if data["quantity"] == "None" or data["quantity"] == "" or data["quantity"] == None:
            del data["quantity"]
        new_drug = Drug(**data)
        new_drug.save()
        return make_response(jsonify({"message": "Successfully created drug"},
                                     new_drug.to_dict()), 200)

    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid json"})
        if data["price"] == "None" or data["price"] == "" or data["price"] == None:
            del data["price"]
        if data["quantity"] == "None" or data["quantity"] == "" or data["quantity"] == None:
            del data["quantity"]
        for attr, value in data.items():
            if attr not in ["id", "created_at", "updated_at"]:
                setattr(drug, attr, value)
        drug.save()
        return make_response(jsonify({"message": "Successfully updated drug"},
                                     drug.to_dict()), 201)

    elif request.method == "DELETE":
        drug.delete()
        storage.save()
        return jsonify({})
