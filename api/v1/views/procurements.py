#!/usr/bin/python3
'''
procurement api endpoints
'''
from flask import jsonify, make_response, request, abort
from models import storage
from models.procurements import Procurement
from models.drugs import Drug
from api.v1.views import ui
import uuid


@ui.route("/procurements", methods=["GET", "POST"])
@ui.route("/procurements/<string:procurement_id>", methods=["GET", "PUT", "DELETE"])
def procurements(procurement_id=None):
    """Handles all default RESTful API actions for Procurement class"""
    if procurement_id:
        procurements = storage.all("Procurement").values()
        procurements_with_id = [procurement.to_dict() for procurement in procurements if procurement.procurement_id == procurement_id]
        if not procurements_with_id:
            abort(404)
        return jsonify(procurements_with_id)

    if request.method == "GET":
        all_procurements = [procurement.to_dict() for procurement in storage.all("Procurement").values()]
        return jsonify(all_procurements)

    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid JSON"})

        vendor_name = data.get("vendor_name")
        drugs = data.get("drugs")

        if not vendor_name or not drugs or not isinstance(drugs, list):
            return jsonify({"message": "Invalid data format"})

        procurement_id = str(uuid.uuid4())

        created_procurements = []

        for drug_data in drugs:
            drug_name = drug_data.get("name")
            quantity = int(drug_data.get("quantity"))
            price = drug_data.get("price")

            if not drug_name or not quantity:
                return jsonify({"message": "Invalid drug data"})

            drug = None
            for existing_drug in storage.all("Drug").values():
                if existing_drug.name == drug_name:
                    drug = existing_drug
                    break

            if drug:
                drug.quantity = int(drug.quantity) + quantity
            else:
                drug = Drug(name=drug_name, quantity=quantity, price=price)
                storage.create(drug)
            
            procurement = Procurement(vendor_name=vendor_name, procurement_id=procurement_id, drug_id=drug.id, name=drug_name, quantity=quantity, price=price)
            
            storage.create(procurement)

            created_procurements.append(procurement.to_dict())  # Serialize each created procurement

        storage.save()  # Save all the created objects at once

        return jsonify({"message": "Successfully created procurements", "procurements": created_procurements})

    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid JSON"})

        for attr, value in data.items():
            if attr not in ["id", "created_at", "updated_at"]:
                setattr(procurement, attr, value)
        storage.save()  # Save the changes to the storage
        return make_response(jsonify({"message": "Successfully updated procurement", **procurement.to_dict()}), 201)

    elif request.method == "DELETE":
        procurements = storage.all("Procurement").values()
        deleted_procurements = []

        for procurement in procurements:
            if procurement.procurement_id == procurement_id:
                deleted_procurements.append(procurement)

        drugs = storage.all("Drug").values()
        for procurement in deleted_procurements:
            drug = next((drug for drug in drugs if drug.id == procurement.drug_id), None)
            if drug:
                drug.quantity -= procurement.quantity
                storage.save(drug)

        for procurement in deleted_procurements:
            storage.delete(procurement)

        storage.save()  # Save the changes to the storage

        return jsonify({"message": "Deleted successfully!"})