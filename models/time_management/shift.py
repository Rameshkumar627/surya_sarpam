# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'draft'), ('allocated', 'Allocated')]
END_INFO = [('current_day', 'Current Day'), ('next_day', 'Next Day')]


class Shift(surya.Sarpam):
    _name = "time.shift"

    name = fields.Char(string="Shift", required=True)
    from_time = fields.Float(string="From Time", required=True)
    till_time = fields.Float(string="Till Time", required=True)
    total_hours = fields.Float(string="Total Hours", compute='get_total_hrs', store=False)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    end_day = fields.Selection(selection=END_INFO, string="End Day")

    def get_total_hrs(self):
        for rec in self:
            if rec.from_time >= rec.till_time:
                rec.total_hours = rec.till_time - rec.from_time
                rec.end_day = "current_day"
            else:
                rec.total_hours = (24 - rec.till_time) + rec.from_time
                rec.end_day = "next_day"

    @api.multi
    def trigger_allocate(self):
        self.write({'progress': 'allocated'})
