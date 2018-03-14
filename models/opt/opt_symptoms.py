# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class OPTSymptoms(surya.Sarpam):
    _name = "opt.symptoms"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

