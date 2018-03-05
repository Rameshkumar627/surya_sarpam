# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Asset

class Asset(surya.Sarpam):
    _name = "comp.asset"

    sequence = fields.Char(string="Sequence", readonly=True)
    product_id = fields.Many2one(comodel_name="product.product", string="Product")

    # Product Info
    model_no = fields.Char(string="")
    serial_no = fields.Char(string="")
    manufacturer = fields.Char(string="")
    supplier = fields.Many2one(comodel_name="", string="")
    category = fields.Many2one(comodel_name="", string="")
    purchased_on = fields.Date(string="")
    purchased_cost = fields.Float(string="")
    manufactured_on = fields
    life_span = ""
    expired_on = ""


    # Purchase Info
    # Handlers Info
    # Service Info
    # Accounts Info
    # Documents
