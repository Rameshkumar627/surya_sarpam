# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

# Time Sheet

PROGRESS_INFO = [('in', 'IN'), ('out', 'OUT')]


class TimeSheet(surya.Sarpam):
    _name = "time.sheet"

    date = fields.Datetime(string="Date", readonly=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", readonly=True)

    def trigger_in(self):
        attendance = self.env["attendance.detail"].search([("employee_id", "=", self.employee_id.id),
                                                           ("attendance_id.date", "=", self.date)])
        actual_in_hrs = datetime.strptime(self.date, "%Y-%m-%d").strftime("%H")
        actual_in_min = datetime.strptime(self.date, "%Y-%m-%d").strftime("%M")
        attendance.actual_in = actual_in_hrs + ((int(actual_in_min)/60) * 100)

    def trigger_out(self):
        current_week = datetime.now().strftime("%U")

        schedule = self.env["schedule.detail"].search([("scheduled_id.week", "=", current_week),
                                            ("employee_id", "=", self.employee_id.id)])

        if schedule.shift.end_day == "current_day":
            new_date = self.date
        elif schedule.shift.end_day == "next_day":
            date = (datetime.strptime(self.date, "%Y-%m-%d")) - timedelta(days=1)
            new_date = date.strftime("%Y-%m-%d")

        attendance = self.env["attendance.detail"].search([("employee_id", "=", self.employee_id.id),
                                                           ("attendance_id.date", "=", self.date)])
        actual_out_hrs = datetime.strptime(new_date, "%Y-%m-%d").strftime("%H")
        actual_out_min = datetime.strptime(new_date, "%Y-%m-%d").strftime("%M")
        attendance.actual_out = actual_out_hrs + ((int(actual_out_min) / 60) * 100)
