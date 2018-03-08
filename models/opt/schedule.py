# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class OPTSchedule(surya.Sarpam):
    _name = "opt.schedule"

    patient_id = fields.Many2one(comodel_name="res.patient", string="Patient")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    start_date = fields.Datetime(string="Start Time")
    end_date = fields.Datetime(string="End Time")
    symptoms = fields.Many2many(comodel_name="opt.symptoms", string="Symptoms")
    others = fields.Text(string="Others")
    scheduled_by = fields.Many2one(comodel_name="hr.employee", string="Scheduled By")
    scheduled_on = fields.Date(string="Scheduled On")



