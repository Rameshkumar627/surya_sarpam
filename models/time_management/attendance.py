# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'Draft'), ('verified', 'Verified')]
ATTENDANCE_INFO = [('half_day', 'Half Day'), ('full_day', 'Full Day'), ('absent', 'Absent')]
PERMISSION_INFO = [('yes', 'YES'), ('no', 'NO')]
SHIFT_INFO = [('yes', 'YES'), ('no', 'NO')]
DAY_INFO = [('working_day', 'Working Day'), ('holiday', 'Holiday')]


class TimeAttendance(surya.Sarpam):
    _name = "time.attendance"

    date = fields.Date(string="Date")
    month_attendance_id = fields.Many2one(comodel_name="time.attendance.month", string="Month")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    attendance_detail = fields.One2many(comodel_name="attendance.detail",
                                        inverse_name="attendance_id",
                                        string="Attendance Detail")
    comment = fields.Text(string="Comment")

    def record_rights(self):
        if self.month_attendance_id:
            if self.month_attendance_id.progress == 'closed':
                raise exceptions.ValidationError('Error! You cannot Cancel/apply attendance since month is closed')

    @api.multi
    def trigger_calculate(self):
        recs = self.attendance_detail
        for rec in recs:
            rec.get_worked_hrs()
            rec.get_attendance_info()
            rec.get_day_info()

    @api.multi
    def trigger_verified(self):
        self.trigger_calculate()
        self.update_leave()
        self.write({"progress": "verified"})

    def update_leave(self):
        recs = self.attendance_detail

        for rec in recs:
            pass


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
    permission = fields.Selection(selection=PROGRESS_INFO, string="Permission")
    day_info = fields.Selection(selection=DAY_INFO, string="Day Info")
    comment = fields.Text(string="Comment")

    attendance_id = fields.Many2one(comodel_name="time.attendance", string="Attendance")

    def record_rights(self):
        if self.attendance_id.month_attendance_id:
            if self.attendance_id.month_attendance_id.progress == 'closed':
                raise exceptions.ValidationError('Error! You cannot Cancel/apply attendance since month is closed')

    def get_worked_hrs(self):
        if self.actual_in >= self.actual_out:
            self.worked_hrs = 24 - (self.actual_out - self.actual_in)
        else:
            self.worked_hrs = self.actual_in - self.actual_out

    @api.depends('worked_hrs')
    def get_attendance_info(self):
        time_conf = self.env["time.configuration"]
        if self.worked_hrs >= time_conf.full_day:
            self.attendance = 'full_day'
        elif self.worked_hrs >= time_conf.half_day:
            self.attendance = 'half_day'
        else:
            self.attendance = 'absent'

    def get_day_info(self):
        day_id = self.env["day.day"].search([("name", "=", self.attendance_id.date)])
        holiday_detail = self.env["holiday.detail"].search([("schedule_id.week", "=", day_id.week_id.id),
                                                            ("shift", "=", self.shift.id)])

        holidays = []

        recs = holiday_detail.holidays
        for rec in recs:
            holidays.append(rec.name)

        if self.attendance_id.date in holidays:
            self.day_info = 'holiday'
        else:
            self.day_info = 'working_day'

