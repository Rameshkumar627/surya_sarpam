# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Month Attendance

PROGRESS_INFO = [('draft', 'Draft'), ('open', 'Open'), ('closed', 'Closed')]


class TimeAttendanceMonth(surya.Sarpam):
    _name = "time.attendance.month"

    sequence = fields.Char(string="Sequence", readonly=True)
    month_id = fields.Many2one(comodel_name="month.month", string="Month", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    time_attendance_ids = fields.One2many(comodel_name="time.attendance",
                                          inverse_name="month_attendance_id",
                                          string="Time Attendance")

    def monthly_closing(self):
        levels = self.env["leave.configuration"].search([("active", "=", True)])

        for level in levels:
            recs = level.leave_configuration_detail

            employees = self.env["hr.employee"].search([("leave_level_id", "=", level.id)])

            for employee in employees:
                data = {}
                data["month_id"] = self.month_id.id
                data["leave_level_id"] = level.id
                data["employee_id"] = employee.id
                data["leave_detail"] = []

                for rec in recs:
                    leave_data = 0

                    leave_detail_obj = self.env["hr.leave.detail"].search([
                        ("hr_leave_id.employee_id", "=", employee.id),
                        ("leave_type_id", "=", rec.leave_type_id.id),
                        ("hr_leave_id.month_id", "=", self.month_id.previous_month.id)])

                    if leave_detail_obj:
                        leave_data = leave_detail_obj.closing_balance

                    data["leave_detail"].append((0, 0, {"leave_type_id": rec.leave_type_id.id,
                                                        "opening_balance": leave_data,
                                                        "increment": rec.increment,
                                                        "order": rec.order}))

                self.env["hr.leave"].create(data)

    def create_closing_leave(self):
        recs = self.env["hr.leave.detail"].search([("hr_leave_id.month_id", "=", self.month_id.previous_month.id)])
        for rec in recs:
            rec.closing_balance = (rec.opening_balance + rec.increment) - rec.leave_taken

    @api.multi
    def trigger_attendance(self):
        self.create_closing_leave()
        self.monthly_closing()
        self.write({"progress": "closed"})
        new_month = self.env["time.attendance.month"].search([("month_id", "=", self.month_id.next_month.id)])
        new_month.write({"progress": "open"})


