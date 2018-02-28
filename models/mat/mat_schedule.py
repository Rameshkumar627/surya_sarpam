# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class MatSchedule(surya.Sarpam):
    _name = "mat.schedule"

    mat_id = fields.Many2one(comodel_name="res.mat", string="Mat")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    start_date = fields.Datetime(string="Start Time")
    end_date = fields.Datetime(string="End Time")
    reason = fields.Text(string="Reason")
    scheduled_by = fields.Many2one(comodel_name="hr.employee", string="Scheduled By")
    scheduled_on = fields.Date(string="Scheduled On")



