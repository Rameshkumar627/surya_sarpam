# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Account Move
class AccountMove(surya.Sarpam):
    _name = "account.move"

    sequence = fields.Char(string="Sequence")
    period = fields.Many2one(comodel_name="period.period")
    reference = fields.Char(string="Reference")
    date = fields.Date(string="Date")
    journal_id = fields.Many2one(comodel_name="account.journal")
    move_detail = fields.One2many(comodel_name="account.move.item",
                                  inverse_name="move_id",
                                  string="Account Move Detail")


class AccountMoveDetail(surya.Sarpam):
    _name = ""

    account_id = ""
    reference = ""
    description = ""
    credit = ""
    debit = ""
    reconcile = ""
    partial_recon = ""







