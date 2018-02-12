# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Salary Rule

PROGRESS_INFO = [('draft', 'draft'), ('allocated', 'Allocated')]
RULE_TYPE = [('fixed', 'Fixed'), ('formula', 'Formula')]


class SalaryRule(surya.Sarpam):
    _name = "salary.rule"

    name = fields.Char(string="Rule", required=True)
    code = fields.Char(string="Code", required=True)
    type = fields.Selection(selection=RULE_TYPE, string="Type", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    fixed = fields.Float(string="Fixed Amount")
    formula = fields.Text(string="Formula")
    comment = fields.Text(string="Comment")



