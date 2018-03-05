# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class OPTTreatment(surya.Sarpam):
    _name = "opt.treatment"

    date = fields.Datetime(string="Date")
    sequence = fields.Char(string="Sequence")
    patient_id = fields.Many2one(comodel_name="res.patient", string="Patient")
    symptoms = fields.Many2many(comodel_name="opt.symptoms", string="Symptoms")
    diagnosis = fields.Many2many(comodel_name="opt.diagnosis", string="Diagnosis")
    medicine_ids = fields.One2many(comodel_name="opt.medicine",
                                   inverse_name="treatment_id",
                                   string="Medicine")
    total_days = fields.Integer(string="Total Days")
    report = fields.Html(string="Report")

    doctor_id = fields.Many2one(comodel_name="hr.employee", string="Doctor")


class OPTMedicine(surya.Sarpam):
    _name = "opt.medicine"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    quantity = fields.Integer(string="Quantity")
    treatment_id = fields.Many2one(comodel_name="opt.treatment", string="Treatment")



