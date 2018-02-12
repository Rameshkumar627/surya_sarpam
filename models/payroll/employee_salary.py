# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Salary Master

SALARY_INFO = [('current_salary', 'Current Salary'), ('previous_salary', '=', 'Previous Salary')]


class Salary(surya.Sarpam):
    _name = "employee.salary"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    employee_uid = fields.Char(string="Employee Id", related="employee_id.employee_uid")
    leave_level_id = fields.Many2one(comodel_name="leave.level",
                                     string="Leave Level",
                                     related="employee_id.leave_level_id")
    doj = fields.Date(string="Date Of Joining", related="employee_id.doj")
    salary_structure = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    pay_slips = fields.One2many(comodel_name="employee.payslip", inverse_name="salary_id", string="Pay Slips")
    incentive_structure = fields.Many2one(comodel_name="salary.incentive", string="Incentive Structure")
    payslip_generation_shift = fields.Many2one(comodel_name="payslip.generation.shift",
                                               string="Payslip Generation Shift")
    previous_salary_details = fields.One2many(comodel_name="employee.salary",
                                              inverse_name="previous_salary_id",
                                              string="Previous Salary Details")






