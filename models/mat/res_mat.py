# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class Mat(surya.Sarpam):
    _name = "res.mat"

    name = fields.Char(string="Name")
    mat_id = fields.Char(string="Mat ID")


