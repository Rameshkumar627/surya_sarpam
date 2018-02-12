# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Month Closing

PROGRESS_INFO = [('draft', 'draft'),
                 ('open', 'Open'),
                 ('closed', 'Closed')]


class EmployeeMonthClose(surya.Sarpam):
    _name = "employee.month.close"

    name = fields.Many2one(string='Month')
    leave_application = fields.One2many(comodel_name='leave.application',
                                        inverse_name='month_id',
                                        string='Leave Application')
    comp_off = ''
    permission = ''
    over_time = ''

    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')

