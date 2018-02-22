# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product

class ProductConfiguration(surya.Sarpam):
    _name = "product.configuration"

    default_location_id = fields.Many2one(comodel_name="stock.location", string="Default Location")
