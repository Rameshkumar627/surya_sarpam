# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class Classification(surya.Sarpam):
    _name = "product.classification"

    name = fields.Char(string="Class")
    code = fields.Char(string="Code")


class SubClassification(surya.Sarpam):
    _name = "product.sub.classification"

    name = fields.Char(string="Sub-Class")
    code = fields.Char(string="Code")
    class_id = fields.Many2one(comodel_name="product.classification", string="Class")
