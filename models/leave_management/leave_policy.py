# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave Policy

class LeavePolicy(surya.Sarpam):
    _name = "leave.policy"
    _rec_name = "year"

    year = fields.Many2one(comodel_name="year.year", string="Year", required=True)
    policy = fields.Html(string="Policy", readonly=True)
