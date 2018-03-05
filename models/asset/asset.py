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
    location_id = fields.Many2one(comodel_name="stock.location", string="Location")
    model_no = fields.Char(string="Model No")
    serial_no = fields.Char(string="Serial No")
    warranty_end = fields.Date(string="Warranty End")
    manufacturer = fields.Char(string="Manufacturer")
    manufactured_on = fields.Date(string="Manufactured On")
    category = fields.Many2one(comodel_name="asset.category", string="Category")
    life_span = fields.Float(string="Life span")
    expired_on = fields.Date(string="Expired On")
    supplier = fields.Many2one(comodel_name="res.partner", string="Supplier")
    purchased_on = fields.Date(string="Purchased On")
    purchased_cost = fields.Float(string="Purchase Price")
    service_id = fields.Many2one(comodel_name="res.partner", string="Service Contact")
    incharge_id = fields.Many2one(comodel_name="hr.employee", string="Incharge")
    service_ids = fields.One2many(comodel_name="asset.service",
                                  inverse_name="asset_id",
                                  string="Service")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    maintenance_ids = fields.One2many(comodel_name="asset.maintenance.alert",
                                      inverse_name="asset_id",
                                      string="Maintenance Alert")








