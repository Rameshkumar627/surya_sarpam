# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock Location

class StockLocation(surya.Sarpam):
    _name = "stock.location"

    name = fields.Char(string="Location")
    code = fields.Char(string="Code")
