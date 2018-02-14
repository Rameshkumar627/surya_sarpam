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

    @api.multi
    def trigger_schedule(self):
        employee_list = []
        month = self.week.month_id.id

        for employee in self.schedule_detail:
            employee_list.append((0, 0, {"employee_id": employee.employee_id.id,
                                         "shift": employee.shift.id}))
        days = self.week.week_detail

        for day in days:
            data = {"date": day.name,
                    "month_attendance_id": month,
                    "attendance_detail": employee_list}

            self.env['time.attendance'].create(data)

    _sql_constraints = [('unique_week_schedule', 'unique (week)', 'Error! Week should not be repeated')]


class TimeScheduleDetail(surya.Sarpam):
    _name = "schedule.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    shift = fields.Many2one(comodel_name="time.shift", string="Shift")
    schedule_id = fields.Many2one(comodel_name="time.schedule", string="Time Schedule")

    _sql_constraints = [('employee_uniq_per_shift_schedule',
                         'unique (employee_id, shift, schedule_id)',
                         'Error! Employee should not repeated')]
