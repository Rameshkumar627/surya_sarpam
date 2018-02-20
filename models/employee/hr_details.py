# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Department

class HRDepartment(surya.Sarpam):
    _name = "hr.department"

    name = fields.Char(string="Department", required=True)
    head = fields.Many2many(comodel_name="hr.employee", string="Department Head")
    members = fields.Many2many(comodel_name="hr.employee", string="Department Members")


# Designation

class HREmployeeDesignation(surya.Sarpam):
    _name = "hr.employee.designation"

    name = fields.Char(string="Designation", required=True)


# Designation

class HREmployeeCategory(surya.Sarpam):
    _name = "hr.employee.category"

    name = fields.Char(string="Category", required=True)


# Contacts

class HRContact(surya.Sarpam):
    _name = "hr.contact"

    name = fields.Char(string="Name")
    relation = fields.Char(string="Relation")
    no = fields.Char(string="Door/Flat No")
    building_name = fields.Char(string="Building Name")
    street_name = fields.Char(string="Street Name")
    locality = fields.Char(string="Locality")
    city = fields.Many2one(comodel_name="res.city", string="State")
    landmark = fields.Char(string="Landmark")
    zip_code = fields.Char(string="Zip Code")
    state = fields.Many2one(comodel_name="res.state", string="State")
    country = fields.Many2one(comodel_name="res.country", string='Country')
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")


# Qualification

class HRQualification(surya.Sarpam):
    _name = "hr.qualification"

    name = fields.Char(string="Name", required=True)
    institution = fields.Char(string="Institution", required=True)
    result = fields.Selection(selection=[], string='Pass/Fail', required=True)
    enrollment_year = fields.Integer(string="Enrollment Year", required=True)
    completed_year = fields.Integer(string="Completed Year")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")


# Experience

class HRExperience(surya.Sarpam):
    _name = "hr.experience"

    name = fields.Char(string="Name", required=True)
    position = fields.Char(string="Position", required=True)
    total_years = fields.Float(string="Total Years", required=True)
    relieving_reason = fields.Text(string="Relieving Reason", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")


# Attachment
class HRAttachment(surya.Sarpam):
    _name = 'hr.attachment'

    name = fields.Char(string="Name", required=True)
    attachment = fields.Binary(string="Attachment", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")


# Leave
class HRLeave(surya.Sarpam):
    _name = "hr.leave"

    month_id = fields.Many2one(comodel_name="month.month", string="Month")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level", required=True)
    leave_detail = fields.One2many(comodel_name="hr.leave.detail",
                                   inverse_name="hr_leave_id",
                                   string="HR Leave Detail")
    total_days = fields.Float(string="Total Days")
    total_present = fields.Float(string="Total Present")
    total_absent = fields.Float(string="Total Absent")
    total_working_days = fields.Float(string="Total Working Days")
    total_holidays = fields.Float(string="Total Holidays")
    total_lop = fields.Float(string="Total LOP")

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")

    _sql_constraints = [('unique_leave_month',
                         'unique (month_id, employee_id)',
                         'Error! Leave month should not be repeated')]


class HRLeaveDetail(surya.Sarpam):
    _name = "hr.leave.detail"

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True, readonly=True)
    opening_balance = fields.Float(string="Opening Balance", readonly=True)
    increment = fields.Float(string="Increment")
    leave_taken = fields.Float(string="Leave Taken")
    closing_balance = fields.Float(string="Closing Balance", readonly=True)
    order = fields.Integer(string="Order Sequence")
    hr_leave_id = fields.Many2one(comodel_name="hr.leave", string="HR Leave")

    _sql_constraints = [('unique_leave_type',
                         'unique (leave_type_id, hr_leave_id)',
                         'Error! Leave Type should not be repeated')]
