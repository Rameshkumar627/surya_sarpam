# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from . import surya
import json


class Religion(surya.Sarpam):
    _name = "res.religion"

    name = fields.Char(string="Religion", required=True)


class Language(surya.Sarpam):
    _name = "res.language"

    name = fields.Char(string="Language", required=True)


