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
    _name = "diagnosis.medicine"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    diagnosis_id = fields.Many2one(comodel_name="opt.diagnosis", string="Treatment")
