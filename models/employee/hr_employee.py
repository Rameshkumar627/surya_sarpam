# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft')]
BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class HrEmployee(surya.Sarpam):
    _name = "hr.employee"

    name = fields.Char(string="Name", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection="BLOOD_GROUP", string="Blood Group")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
    work_email = fields.Char(string="Work Email")
    work_mobile = fields.Char(string="Work Mobile", required=True)
    date_of_joining = fields.Date(string="Date of Joining", required=True)
    date_of_relieving = fields.Date(string="Date of Relieving")
    department = fields.Many2one(comodel_name="hr.department", string="Department")
    designation = fields.Many2one(comodel_name="hr.employee.designation", string="Designation")
    reporting_to = fields.Many2one(comodel_name="hr.employee", string="Reporting To")
    employee_category = fields.Many2one(comodel_name="hr.employee.category", string="Employee Category")
    gender = fields.Selection(selection=GENDER, string="Gender")
    caste = fields.Char(string="Caste")
    religion = fields.Many2one(comodel_name="res.religion", string="Religion")
    physically_challenged = fields.Boolean(string="Physically Challenged")

    nationality = fields.Many2one(comodel_name="res.country")
    mother_toungue = fields.Many2one(comodel_name="res.language", string="Mother Toungue")
    language_known = fields.Many2many(comodel_name="res.language", string="Language Known")
    personnel_mobile = fields.Char(string="Personnel Mobile")
    personnel_email = fields.Char(string="Personnel Email")
    contact_address = fields.Char(string="Contact Address")
    is_contact_differ_permanent = fields.Boolean(string="Is Contact Address From Permanent Address")
    permanent_address = fields.Char(string="Permanent Address")
    family_members = fields.One2many(comodel_name="hr.contact",
                                     inverse_name="employee_id",
                                     string="Family Members")
    qualification = fields.One2many(comodel_name="hr.qualification",
                                    inverse_name="employee_id",
                                    string="Family Members")
    experience = fields.One2many(comodel_name="hr.experience",
                                 inverse_name="employee_id",
                                 string="Family Members")
    account_info = fields.One2many(comodel_name="hr.account.info",
                                   inverse_name="employee_id",
                                   string="Family Members")
    attachment = fields.One2many(comodel_name="hr.attachment",
                                 inverse_name="employee_id",
                                 string="Family Members")
    leave = fields.One2many(comodel_name="hr.leave",
                            inverse_name="employee_id",
                            string="Leave")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")


