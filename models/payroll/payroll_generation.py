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
                    "lop_days": 0}

            payroll = self.env["employee.payslip"].create(data)
            payroll.trigger_payslip()


class PayrollGenerationDetail(surya.Sarpam):
    _name = "payroll.generation.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    generation_id = fields.Many2one(comodel_name="payroll.generation", string="Payroll Generation")

