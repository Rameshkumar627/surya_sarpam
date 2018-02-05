# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft')]


class HrEmployee(surya.Sarpam):
    _name = "hr.employee"

    name = fields.Char(string="Name")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')


