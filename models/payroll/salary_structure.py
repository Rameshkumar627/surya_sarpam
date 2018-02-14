# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Salary Structure

PROGRESS_INFO = [('draft', 'draft'), ('allocated', 'Allocated')]


class SalaryStructure(surya.Sarpam):
    _name = "salary.structure"

    name = fields.Char(string="Salary Structure", required=True)
    code = fields.Char(string="Code", required=True)
    structure_detail = fields.One2many(comodel_name="salary.structure.detail",
                                       inverse_name="structure_id",
                                       string="Salary Structure")
    comment = fields.Text(string="Comment")


class SalaryStructureDetail(surya.Sarpam):
    _name = "salary.structure.detail"

    order = fields.Integer(string="Order")
    rule_id = fields.Many2one(comodel_name="salary.rule", string="Salary Rule")
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")







