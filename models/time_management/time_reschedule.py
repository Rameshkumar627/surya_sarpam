# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave Application
# Time Reschedule

PROGRESS_INFO = [('draft', 'draft'),
                 ('wfa', 'Waiting For Approval'),
                 ('approved', 'Approved'),
                 ('cancelled', 'Cancelled')]


class TimeReschedule(surya.Sarpam):
    _name = "time.reschedule"
    _rec_name = "employee_id"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string='From Date', required=True)
    shift = fields.Many2one(comodel_name="time.shift", string="Shift", required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    created_on = fields.Date(string='Created On', readonly=True)
    created_by = fields.Many2one(comodel_name='hr.employee', string='Created By', readonly=True)
    approved_on = fields.Date(string='Approved On', readonly=True)
    approved_by = fields.Many2one(comodel_name='hr.employee', string='Approved By', readonly=True)
    attendance_month_id = fields.Many2one(comodel_name='time.attendance.month', string='Month', readonly=True)

    def record_rights(self):
        if self.attendance_month_id:
            if self.attendance_month_id.progress == 'closed':
                raise exceptions.ValidationError('Error! You cannot Cancel/apply Shift Reschedule since month is closed')

    def default_vals_creation(self, vals):
        vals['created_on'] = datetime.now().strftime("%Y-%m-%d")
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals['created_by'] = employee_id.id
        vals['employee_id'] = employee_id.id

        return vals

    @api.multi
    def trigger_wfa(self):
        self.check_progress_rights()

        month = (datetime.strptime(self.date, "%Y-%m-%d")).strftime("%m-%Y")
        month_id = self.env['time.attendance.month'].search([('month_id.name', '=', month)])

        if not month_id:
            raise exceptions.ValidationError("Error! Month is not available")
        self.record_rights()

        data = {'sequence': self.env['ir.sequence'].sudo().next_by_code('compoff.application'),
                'attendance_month_id': month_id.id,
                'progress': 'wfa'}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        attendance = self.env["attendance.detail"].search([('employee_id', '=', 0),
                                                           ('attendance_id.date', '=', self.date)])

        if attendance:
            attendance.write({"shift": self.shift.id})
        else:
            raise exceptions.ValidationError("Error! Week is not scheduled please check Time Shedule")

        data = {'approved_on': datetime.now().strftime("%Y-%m-%d"),
                'approved_by': self.env.user.id,
                'progress': 'approved'}
        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        data = {'approved_on': datetime.now().strftime("%Y-%m-%d"),
                'approved_by': self.env.user.id,
                'progress': 'cancelled'}
        self.write(data)

