#!/usr/bin/env python3

"""Module implements all invoices restful api operations"""

from flask import Flask, request, jsonify, abort
from models import storage
from models.invoices import Invoice
from api.v1.views import ui


@ui.route("/invoices/<string:patient_id>", methods=["POST"])
@ui.route("/prescription_invoice/<string:prescription_id>", methods=["POST"])
@ui.route("/invoice/<string:invoice_id>", methods=["GET", "PUT", "DELETE"])
def invoices(patient_id=None, invoice_id=None, prescription_id=None):
    """Method implements all restful api operations"""
    if patient_id is None and invoice_id is None and prescription_id is None:
        abort(400)
    if patient_id:
        patient = storage.get("Patient", patient_id)
        if patient is None:
            return
    elif invoice_id:
        invoice = storage.get("Invoice", invoice_id)
        if invoice is None:
            return
    elif prescription_id:
        prescription = storage.get("Prescription", prescription_id)
        if prescription is None:
            return
    if request.method == "POST":
        if prescription_id:
            patient_id = prescription.patient_id
            new_invoice = Invoice(prescription_id=prescription_id, patient_id=patient_id)
        elif patient_id:
            new_invoice = Invoice(patient_id=patient_id)
        new_invoice.save()
        return jsonify(new_invoice.to_dict()), 201
    elif request.method == "GET":
        return jsonify(invoice.to_dict()), 200
    elif request.method == "DELETE":
        storage.delete(invoice)
        return jsonify({})
    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"message": "data not submitted"})
        else:
            for key, value in data.values():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(invoice, key, value)
            invoice.save()
            return jsonify(invoice.to_dict()), 200