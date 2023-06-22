#!/usr/bin/python3

"""Modules implements tests for patient class"""

import unittest
import inspect
from models.patients import Patient
from models.drug import Drug
from models.payments import Payment
from models import storage
from models.base_model import BaseModel
import pep8 as pycodestyle
module_doc = patients.__doc__


class test_patient(unittest.TestCase):
    """class implements tests for patient class"""
    @classmethod
    def setUpClass(self):
        """set up any resources or objects that are needed for the tests"""
        self.all_methods = inspect.getmembers(Patient, inspect.isfunction)

    def test_pycodestyle_conformance(self):
        """Tests styling compliance"""
        paths = ["models/patients.py", "tests/tests_models/test_patients.py"]
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

