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


class OfficeBill(surya.Sarpam):
    _name = "office.bill"
    _rec_name = "employee_id"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string='From Date', required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    amount = fields.Float(string="Amount")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    created_on = fields.Date(string='Created On', readonly=True)
    created_by = fields.Many2one(comodel_name='hr.employee', string='Created By', readonly=True)
    approved_on = fields.Date(string='Approved On', readonly=True)
    approved_by = fields.Many2one(comodel_name='hr.employee', string='Approved By', readonly=True)

    def default_vals_creation(self, vals):
        vals['created_on'] = datetime.now().strftime("%Y-%m-%d")
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals['created_by'] = employee_id.id
        vals['employee_id'] = employee_id.id

        return vals

    @api.multi
    def trigger_wfa(self):
        self.check_progress_rights()

        data = {'sequence': self.env['ir.sequence'].sudo().next_by_code('employee.voucher'),
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

