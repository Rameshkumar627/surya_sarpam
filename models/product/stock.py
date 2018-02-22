# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock

class Stock(surya.Sarpam):
    _name = "stock.stock"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    location_id = fields.Many2one(comodel_name="stock.location", streing="Location")
    quantity = fields.Float(string="Quantity")
