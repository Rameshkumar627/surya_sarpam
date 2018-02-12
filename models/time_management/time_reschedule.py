# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [("draft", "Draft"), ("approved", "Approved")]


# Time Reschedule

class TimeReSchedule(surya.Sarpam):
    _name = "time.reschedule"

    date = fields.Date(string="Date", required=True)
    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employee", required=True)
    shift = fields.Many2one(comodel_name="time.shift", string="Shift", required=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")

    @api.multi
    def trigger_approved(self):
        employees = self.employee_ids

        recs = []

        for employee in employees:
            attendance_obj = self.env["attendance.detail"].search([("employee_id", "=", employee.id),
                                                                   ("attendance_id.date", "=", self.date)])

            if attendance_obj:
                recs.append(attendance_obj)
            else:
                raise exceptions.ValidationError("Error! No attendance scheduled is found")

        for rec in recs:
            rec.write({"shift_change": "yes", "shift": self.shift.id})
        self.write({"progress": "approved"})
