#!/usr/bin/python3
"""Implements tests for Drug Class"""
import unittest
from models import storage
from models.drugs import Drug
from models.patients import Patient
from models.patients_drugs import PatientDrug
from models import storage_env
from api.v1.views import ui
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views.patients_drugs import patient_drug

class TestDrug(unittest.TestCase):
    """Tests Drug Class"""
    def setUp(self):
        """Sets up test environment"""
        self.app = Flask(__name__)
        self.app.register_blueprint(ui)
        self.client = self.app.test_client()

    def test_get_patient_drugs(self):
        """Tests GET /patient/<patient_id>/drug"""
        patient = Patient()
        patient.save()
        drug = Drug()
        drug.save()
        patient_drug = PatientDrug()
        patient_drug.patient_id = patient.id
        patient_drug.drug_id = drug.id
        patient_drug.save()
        response = self.client.get("/api/v1/patient/{}/drug".format(patient.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [drug.to_dict()])

    def test_post_patient_drug(self):
        """Tests POST /patient/<patient_id>/drug/<drug_id>"""
        patient = Patient()
        patient.save()
        drug = Drug()
        drug.save()
        response = self.client.post("/api/v1/patient/{}/drug/{}".format(patient.id, drug.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, drug.to_dict())

    def test_delete_patient_drug(self):
        """Tests DELETE /patient/<patient_id>/drug/<drug_id>"""
        patient = Patient()
        patient.save()
        drug = Drug()
        drug.save()
        patient_drug = PatientDrug()
        patient_drug.patient_id = patient.id
        patient_drug.drug_id = drug.id
        patient_drug.save()
        response = self.client.delete("/api/v1/patient/{}/drug/{}".format(patient.id, drug.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def tearDown(self):
        """Tears down test environment"""
        storage.delete_all(storage_env)

    def test_create_drug(self):
        """Tests Drug creation"""
        drug = Drug()
        drug.name = "Test Drug"
        drug.save()
        self.assertEqual(drug.name, "Test Drug")

    def test_attributes(self):
        """Tests Drug attributes"""
        drug = Drug()
        drug.name = "Test Drug"
        drug.save()
        self.assertEqual(drug.name, "Test Drug")
        self.assertEqual(drug.id, drug.id)
        self.assertEqual(drug.created_at, drug.created_at)
        self.assertEqual(drug.updated_at, drug.updated_at)

    def test_to_dict(self):
        """Tests Drug to_dict"""
        drug = Drug()
        drug.name = "Test Drug"
        drug.save()
        self.assertEqual(drug.to_dict()["name"], "Test Drug")
        self.assertEqual(drug.to_dict()["id"], drug.id)
        self.assertEqual(drug.to_dict()["created_at"], drug.created_at.isoformat())
        self.assertEqual(drug.to_dict()["updated_at"], drug.updated_at.isoformat())

    def test_str(self):
        """Tests Drug __str__"""
        drug = Drug()
        drug.name = "Test Drug"
        drug.save()
        self.assertEqual(str(drug), "[Drug] ({}) {}".format(drug.id, drug.__dict__))