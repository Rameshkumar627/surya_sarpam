# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock

PROGRESS_INFO = [('in', 'In'), ('out', 'OUT'), ('internal', 'Internal')]


class StockMove(surya.Sarpam):
    _name = "stock.move"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    source_id = fields.Many2one(comodel_name="stock.location", string="Source")
    destination_id = fields.Many2one(comodel_name="stock.location", string="Destination")
    quantity = fields.Float(sttring="Quantity")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
