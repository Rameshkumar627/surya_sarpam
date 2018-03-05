# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class OPTDiagnosis(surya.Sarpam):
    _name = "opt.diagnosis"

    name = fields.Char(string="Name")
    medicine_ids = fields.One2many(comodel_name="diagnosis.medicine",
                                   inverse_name="diagnosis_id", string="Medicine")


class DiagnosisMedicine(surya.Sarpam):
    product_id = ""
    morning = ""
    noon