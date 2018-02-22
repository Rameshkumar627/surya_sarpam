# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Tax


class Tax(surya.Sarpam):
    _name = "product.tax"

    name = fields.Char(string="Tax")
    value = fields.Char(string="Value")
