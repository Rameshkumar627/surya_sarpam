# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# ward
TRAVEL_TYPE = [('emergency', 'Emergency'), ('ordinary', 'Ordinary')]
BILLING_INFO = [('draft', 'Draft'), ('billed', 'Billed')]
PROGRESS_INFO = [('draft', 'Draft'), ('assigned', 'Assigned'),
                 ('completed', 'Completed'), ('cancel', 'Cancel')]


class Ward(surya.Sarpam):
    _name = "ipt.ward"

    name = fields.Char(string="Ward")
    bed_ids = fields.Many2one(comodel_name="ipt.bed", inverse_name="ward_id", string="Bed")


class Bed(surya.Sarpam):
    _name = "ipt.bed"

    name = fields.Char(string="Bed")
    rate = fields.Float(string="Rate")
    ward_id = fields.Many2one(comodel_name="ipt.ward", string="Ward")
