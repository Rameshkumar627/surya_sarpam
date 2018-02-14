# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Payslip

class PayrollPolicy(surya.Sarpam):
    _name = "payroll.policy"

    year_id = fields.Many2one(comodel_name="year.year", string="Year")
    policy = fields.Html(string="Policy", readonly=True)
