# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'), ('admitted', 'Admitted'), ('cancelled', 'Cancelled')]
PATIENT_STATUS = [('serious', 'Serious'), ('normal', 'Normal')]


class Admission(surya.Sarpam):
    _name = "ipt.admission"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    patient_id = fields.Many2one(comodel_name="res.mat")
    reason = fields.Many2one(comodel_name="ipt.admission.reason", string="Reason")
    admission_by = fields.Many2one(comodel_name="hr.employee", string="Admission By")
    admission_on = fields.Datetime(string="Admission On")
    admitted_by = fields.Many2one(comodel_name="hr.contact", string="Admitted By")
    patient_status = fields.Selection(selection=PATIENT_STATUS, string="Patient Status")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    comment = fields.Text(string="Comment")

