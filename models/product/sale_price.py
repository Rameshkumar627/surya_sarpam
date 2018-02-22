# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Sale

class ProductSale(surya.Sarpam):
    _name = "product.sale"

    from_date = fields.Date(string="From Date")
    till_date = fields.Date(string="Till Date")
    unit_price = fields.Float(string="Unit Price")
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
