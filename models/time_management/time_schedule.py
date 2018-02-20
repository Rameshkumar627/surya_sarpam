# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, date, timedelta
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'Draft'), ('scheduled', 'Scheduled')]


class TimeSchedule(surya.Sarpam):
    _name = "time.schedule"

    sequence = fields.Char(string="Schedule", readonly=True)
    week = fields.Many2one(comodel_name="week.week", string="Week", required=True)
    schedule_detail = fields.One2many(comodel_name="schedule.detail",
                                      inverse_name="schedule_id",
                                      string="Schedule Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress')

    def check_month_attendance(self, month_attendance_id):
        if not month_attendance_id:
            raise exceptions.ValidationError("Attendance Month is not present")

        if month_attendance_id.progress == 'closed':
            raise exceptions.ValidationError('Error! You cannot Schedule the week since month is closed')

    @api.multi
    def trigger_schedule(self):
        employee_list = []

        for employee in self.schedule_detail:
            employee_list.append((0, 0, {"employee_id": employee.employee_id.id,
                                         "shift": employee.shift.id}))
        days = self.week.day_detail

        for day in days:
            month_attendance_id = self.env["time.attendance.month"].search([("month_id", "=", day.month_id.id)])

            self.check_month_attendance(month_attendance_id)

            data = {"date": day.name,
                    "month_attendance_id": month_attendance_id.id,
                    "attendance_detail": employee_list}

            self.env['time.attendance'].create(data)

    _sql_constraints = [('unique_week_schedule', 'unique (week)', 'Error! Week should not be repeated')]


class TimeScheduleDetail(surya.Sarpam):
    _name = "schedule.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    shift = fields.Many2one(comodel_name="time.shift", string="Shift", required=True)
    schedule_id = fields.Many2one(comodel_name="time.schedule", string="Time Schedule")

    _sql_constraints = [('employee_uniq_per_shift_schedule',
                         'unique (employee_id, shift, schedule_id)',
                         'Error! Employee should not repeated')]
