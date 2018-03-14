# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Account Journal

class AccountJournal(surya.Sarpam):
    _name = "account.journal"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    default_debit_account = fields.Many2one(comodel_name="account.account", string="Debit Account")
    default_credit_account = fields.Many2one(comodel_name="account.account", string="Credit Account")




