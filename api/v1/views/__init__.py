#!/usr/bin/python3

"""API Blueprint"""
from flask import Blueprint

ui = Blueprint("ui", __name__, url_prefix='/api/v1')

from api.v1.views.patients import *
from api.v1.views.drugs import *
from api.v1.views.payments import *
from api.v1.views.patients_drugs import *
from api.v1.views.users import *
from api.v1.views.prescriptions import *
from api.v1.views.invoices import *
from api.v1.views.prescribed_drugs import *
from api.v1.views.services import *
from api.v1.views.chatgpt import *
from api.v1.views.procurements import *
from api.v1.views.invoice_services import *
