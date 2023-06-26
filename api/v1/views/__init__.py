#!/usr/bin/python3

"""API Blueprint"""
from flask import Blueprint

ui = Blueprint("ui", __name__, url_prefix='/api/v1')

from api.v1.views.patients import *
from api.v1.views.drugs import *
from api.v1.views.payments import *
from api.v1.views.patients_drugs import *
from api.v1.views.users import *
