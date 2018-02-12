# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'Draft'), ('verified', 'Verified')]
ATTENDANCE_INFO = [('present', 'Present'), ('absent', 'Absent')]
ARRIVAL_INFO = [('late', 'Late'), ('on_time', 'On Time')]
PERMISSION_INFO = [('yes', 'YES'), ('no', 'NO')]
SHIFT_INFO = [('yes', 'YES'), ('no', 'NO')]


class TimeAttendance(surya.Sarpam):
    _name = "time.attendance"

    date = fields.Date(string="Date")
    month_attendance_id = fields.Many2one(comodel_name="time.attendance.month", string="Month")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    attendance_detail = fields.One2many(comodel_name="attendance.detail",
                                        inverse_name="attendance_id",
                                        string="Attendance Detail")
    comment = fields.Text(string="Comment")

    @api.multi
    def trigger_calculate(self):
        recs = self.attendance_detail
        for rec in recs:
            rec.get_worked_hrs()
            rec.get_attendance_info()
            rec.get_arrival_info()
            rec.get_permission_info()

    @api.multi
    def trigger_verified(self):
        self.trigger_calculate()
        self.write({"progress": "verified"})


class AttendanceDetail(surya.Sarpam):
    _name = "attendance.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    shift = fields.Many2one(comodel_name="time.shift", string="Shift", readonly=True)
    shift_change = fields.Selection(selection=SHIFT_INFO, string="Attendance")
    expected_in = fields.Float(string="Expected IN", related="shift.from_time")
    actual_in = fields.Float(string="Actual IN")
    expected_out = fields.Float(string="Expected OUT", related="shift.till_time")
    actual_out = fields.Float(string="Actual OUT")
    working_hrs = fields.Float(string="Working Hours", related="shift.total_hours")
    worked_hrs = fields.Float(string="Worked Hours")
    attendance = fields.Selection(selection=ATTENDANCE_INFO, string="Attendance")
    arrival = fields.Selection(selection=ARRIVAL_INFO, string="Arrival")
    permission = fields.Selection(selection=PROGRESS_INFO, string="Permission")
    comment = fields.Text(string="Comment")

    attendance_id = fields.Many2one(comodel_name="time.attendance", string="Attendance")

    def get_worked_hrs(self):
        if self.actual_in >= self.expected_out:
            self.worked_hrs = self.till_time - self.from_time
        else:
            self.worked_hrs = (24 - self.expected_out) + self.actual_in

    def get_attendance_info(self):
        if self.actual_in:
            self.attendance = "present"

    def get_arrival_info(self):
        if (self.actual_in - self.expected_in) > 0:
            self.arrival = "on_time"
        else:
            self.arrival = "late"

    def get_permission_info(self):
        pass



