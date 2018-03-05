# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Low Stock
PROGRESS_INFO = [("draft", "Draft"), ("indent_raised", "Indent Raised")]


class LowStock(surya.Sarpam):
    _name = "low.stock"

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
