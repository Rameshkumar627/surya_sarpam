# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave Application
# Leave Comp-Off
# Over Time
# Permission
# Time Reschedule

PROGRESS_INFO = [('draft', 'draft'),
                 ('wfa', 'Waiting For Approval'),
                 ('approved', 'Approved'),
                 ('cancelled', 'Cancelled')]


class LeaveApplication(surya.Sarpam):
    _name = "leave.application"
    _rec_name = "employee_id"

    sequence = fields.Char(string='Sequence', readonly=True)
    from_date = fields.Date(string='From Date', required=True)
    till_date = fields.Date(string='Till Date', required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    created_on = fields.Date(string='Created On', readonly=True)
    created_by = fields.Many2one(comodel_name='hr.employee', string='Created By', readonly=True)
    approved_on = fields.Date(string='Approved On', readonly=True)
    approved_by = fields.Many2one(comodel_name='hr.employee', string='Approved By', readonly=True)
    month_id = fields.Many2one(comodel_name='employee.month', string='Month', readonly=True)

    def check_date(self):
        message = 'Please Check the given Date'

        # 1. from_date < till_date
        if not (self.from_date < self.till_date):
            raise exceptions.ValidationError(message)

        # 2. date within month
        from_date_month = (datetime.strptime(self.from_date, "%Y-%m-%d")).strftime("%m-%Y")
        till_date_month = (datetime.strptime(self.till_date, "%Y-%m-%d")).strftime("%m-%Y")

        if not (from_date_month == till_date_month):
            raise exceptions.ValidationError(message)

    def record_rights(self):
        if self.month_id:
            if self.month_id == 'completed':
                raise exceptions.ValidationError('Error! You cannot Cancel the record since month is closed')

    def default_vals_creation(self, vals):
        month_year = (datetime.strptime(self.from_date, "%Y-%m-%d")).strftime("%m-%Y")

        vals['month_id'] = self.env['employee.month'].search([('name', '=', month_year)])
        vals['created_on'] = datetime.now().strftime("%Y-%m-%d")
        vals['created_by'] = self.env.user.id

        return vals

    @api.multi
    def trigger_wfa(self):
        self.check_progress_rights()
        self.check_date()
        data = {'sequence': self.env['ir.sequence'].sudo().next_by_code('leave.application'),
                'progress': 'wfa'}
        self.write(data)

    @api.multi
    def trigger_approved(self):
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

