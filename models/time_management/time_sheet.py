# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

# Time Sheet

PROGRESS_INFO = [('in', 'IN'), ('out', 'OUT')]


class TimeSheet(surya.Sarpam):
    _name = "time.sheet"

    date = fields.Datetime(string="Date", readonly=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", readonly=True)


