# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Payslip

class Payslip(surya.Sarpam):
    _name = "employee.payslip"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True)
    employee_uid = fields.Char(string="Employee Id", related="employee_id.employee_uid")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    doj = fields.Date(string="Date Of Joining", related="employee_id.doj")
    salary_structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    generation_id = fields.Many2one(comodel_name="payroll.generation", string="Payslip Generation")

    total_days = fields.Float(string="Total Days")
    absent_days = fields.Float(string="Absent Days")
    lop_days = fields.Float(string="LOP Days")

    payslip_detail = fields.One2many(comodel_name="payslip.detail",
                                     inverse_name="payslip_id",
                                     string="Payslip Detail")

    @api.multi
    def trigger_payslip(self):
        structure = self.salary_structure_id.structure_detail
        rules = structure.sorted(key=lambda r: r.order)

        rule_dict = {}
        for rule in rules:
            if rule.rule_id.type == "fixed":
                rule_dict[rule.rule_id.code] = rule.rule_id.fixed
            elif rule.rule_id.type == "formula":
                try:
                    rule_dict[rule.rule_id.code] = eval(rule.rule_id.formula, rule_dict)
                except (NameError, ZeroDivisionError):
                    raise exceptions.ValidationError("Error! Please Check the Salrary Rule Formula")

            data = {"rule_id": rule.id,
                    "amount": rule_dict[rule.rule_id.code]}

            self.payslip_detail.create(data)


class PayslipDetail(surya.Sarpam):
    _name = "payslip.detail"

    rule_id = fields.Many2one(comodel_name="salary.rule", string="Salary Rule", required=True)
    amount = fields.Float(string="Amount")
    payslip_id = fields.Many2one(comodel_name="employee.payslip", string="Payslip")

