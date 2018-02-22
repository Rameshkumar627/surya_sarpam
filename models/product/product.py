# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product

class Product(surya.Sarpam):
    _name = "product.product"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    parent_id = fields.Many2one(comodel_name="product.product", string="Parent")
    child_id = fields.One2many(comodel_name="product.product", inverse_name="parent_id", string="Child")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM")
    sale_price = fields.One2many(comodel_name="product.sale",
                                 inverse_name="product_id",
                                 string="Sale Price")

    on_hand_qty = fields.Float(string="On Hand Qty", compute="get_stock_on_hand")
    incoming_shipment = fields.Float(string="Incoming Shipment")

    def get_stock_on_hand(self):
        for rec in self:
            qty = 0
            stocks = self.env["stock.stock"].search([("product_id", "=", rec.id)])
            for stock in stocks:
                qty = qty + stock.quantity
            rec.on_hand_qty = qty

    # Special Button
    def smart_stock(self):
        view_id = self.env['ir.model.data'].get_object_reference('surya_sarpam', 'view_stock_stock_tree')[1]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Location Wise Stock',
            'view_mode': 'tree',
            'view_type': 'tree,form',
            'view_id': view_id,
            'domain': [('product_id', '=', self.id)],
            'res_model': 'stock.stock',
            'target': 'current',
        }

