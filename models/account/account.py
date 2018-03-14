# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Account Ledger

class Account(surya.Sarpam):
    _name = "h.account.account"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    description = fields.Char(string="Description")

