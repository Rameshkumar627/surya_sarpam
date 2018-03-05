# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class AssetService(surya.Sarpam):
    _name = "asset.service"

    date = fields.Date(string="Date")
    service_by = fields.Many2one(comodel_name="res.partner", string="Service By")
    service_person = fields.Char(string="Service Person")
    description = fields.Text(string="Description")
    amount = fields.Float(string="Amount")
    comment = fields.Text(string="Comment")
    asset_id = fields.Many2one(comodel_name="comp.asset", string="Asset")


class AssetMaintenanceAlert(surya.Sarpam):
    _name = "asset.maintenance.alert"

    date = fields.Date(string="Date")
    asset_id = fields.Many2one(comodel_name="comp.asset", string="Asset")
