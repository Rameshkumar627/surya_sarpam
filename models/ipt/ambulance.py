# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Purchase Indent
TRAVEL_TYPE = [('emergency', 'Emergency'), ('ordinary', 'Ordinary')]
BILLING_INFO = [('draft', 'Draft'), ('billed', 'Billed')]
PROGRESS_INFO = [('draft', 'Draft'), ('assigned', 'Assigned'),
                 ('completed', 'Completed'), ('cancel', 'Cancel')]


class Ambulance(surya.Sarpam):
    _name = "ipt.ambulance"

    date = fields.Date(string="Date", readonly=True)
    driver_id = fields.Many2one(comodel_name="hr.employee", string="Driver", required=True)
    staff_ids = fields.Many2many(comodel_name="hr.employee", string="Staff(s)")
    from_location = fields.Char(string="From Location")
    till_location = fields.Char(string="Till Location")
    duration = fields.Float(string="Duration (Hrs)")
    distance = fields.Float(string="Distance (KM)")
    travel_type = fields.Selection(selection=TRAVEL_TYPE, string="Travel Type")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    billing = fields.Selection(selection=BILLING_INFO, string="Billing")
    comment = fields.Text(string="Comment")



