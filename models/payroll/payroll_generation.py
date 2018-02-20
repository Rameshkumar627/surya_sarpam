# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Salary Rule

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]


class PayrollGeneration(surya.Sarpam):
    _name = "payroll.generation"

    month_id = fields.Many2one(comodel_name="month.month", string="Month")
    payroll_generation_detail = fields.One2many(comodel_name="payroll.generation.detail",
                                                inverse_name="generation_id",
                                                string="Payroll Generation  Detail")

    def record_rights(self):
        attn_month = self.env["time.attendance.month"].search([("month_id", "=", self.month_id.id)])
        if attn_month.progress != 'closed':
            raise exceptions.ValidationError('Error! You cannot Create payslip since month is not closed')

    def update_leave_taken(self):
        pass

    def attendance_calculation(self, employee_id):
        recs = self.env[("attendance.detail")].search([("employee_id", "=", employee_id),
                                                       ("attendance_id.month_attendance_id", "=",self.month_id.id)])

        present = absent = total_days = lop = 0
        for rec in recs:
            total_days = total_days + 1
            if rec.attendance == 'half_day':
                present = present + .5
            elif rec.attendance == 'full_day':
                present = present + 1
            elif rec.attendance == 'absent':
                absent = absent + 1

        for absent_day in range(absent):
            pass

        return present, absent, total_days

    @api.multi
    def trigger_generation(self):
        recs = self.payroll_generation_detail

        for rec in recs:
            employee_salary = self.env["employee.salary"].search([("employee_id", "=", rec.employee_id.id)])

            data = {"employee_id": rec.employee_id.id,
                    "leave_level_id": rec.employee_id.leave_level_id.id,
                    "doj": rec.employee_id.doj,
                    "salary_structure_id": employee_salary.salary_structure.id,
                    "generation_id": self.id,
                    "total_days": 0,
                    "absent_days": 0,
                    "month_id": self.month_id.id,
                    "lop_days": 0}

            payslip = self.env["employee.payslip"].search([("employee_id", "=", rec.employee_id.id),
                                                           ("month_id", "=", self.month_id.id)])

            if not payslip:
                payroll = self.env["employee.payslip"].create(data)
                payroll.trigger_payslip()


class PayrollGenerationDetail(surya.Sarpam):
    _name = "payroll.generation.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    generation_id = fields.Many2one(comodel_name="payroll.generation", string="Payroll Generation")

