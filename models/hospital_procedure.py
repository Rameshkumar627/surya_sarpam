# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from . import surya
import json


# Hospital Procedure

class HospitalProcedure(surya.Sarpam):
    _name = "hospital.procedure"
    _rec_name = "name"

    name = fields.Char(string="name")
    procedure = fields.Html(string="Procedure", readonly=True)
