# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock

PROGRESS_INFO = [('in', 'In'), ('out', 'OUT'), ('internal', 'Internal')]


class StockMove(surya.Sarpam):
    _name = "stock.move"

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True)
    source_id = fields.Many2one(comodel_name="stock.location", string="Source")
    destination_id = fields.Many2one(comodel_name="stock.location", string="Destination")
    quantity = fields.Float(sttring="Quantity")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")

    def default_vals_creation(self, vals):
        if vals["source_id"]:
            source_id = self.env["stock.location"].search([("id", "=", vals["source_id"])])

            stock = self.env["stock.stock"].search([("product_id", "=", vals["product_id"]),
                                                    ("location_id", "=", source_id.id)])

            if not stock:
                stock = self.env["stock.stock"].create({"product_id": vals["product_id"],
                                                        "location_id": source_id.id})

            stock.quantity = stock.quantity - vals["quantity"]

        if vals["destination_id"]:
            destination_id = self.env["stock.location"].search([("id", "=", vals["destination_id"])])

            stock = self.env["stock.stock"].search([("product_id", "=", vals["product_id"]),
                                                    ("location_id", "=", destination_id.id)])

            if not stock:
                stock = self.env["stock.stock"].create({"product_id": vals["product_id"],
                                                        "location_id": destination_id.id})

            stock.quantity = stock.quantity + vals["quantity"]

        return vals

    @api.constrains
    def _validate_quantity(self):
        if self.quantity <= 0:
            raise exceptions.ValidationError("Error! Stock Move needs quantity")
