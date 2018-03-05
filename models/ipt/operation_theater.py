# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Operation Theater
PROGRESS_INFO = [('draft', 'Draft'), ('booked', 'Booked'),
                 ('cancelled', 'Cancelled'), ('completed', 'Completed')]


class OperationTheater(surya.Sarpam):
    _name = "operation.theater"

    sequence = fields.Char(string="Sequence")
    date = fields.Datetime(string="Date")
    booked_by = fields.Many2one(comodel_name="hr.employee", string="Booked By")
    booked_on = fields.Date(string="Booked On")
    doctor_ids = fields.Many2many(comodel_name="hr.employee", string="Doctor(s)")
    staff_ids = fields.Many2many(comodel_name="hr.employee", string="Staff(s)")
    report = fields.Many2many(comodel_name="ir.attachment", string="Report")
    procedure = fields.Many2one(comodel_name="hospital.procedure", string="OT Procedure")
    docs = fields.Many2many(comodel_name="ir.attachment", string="Docs")


