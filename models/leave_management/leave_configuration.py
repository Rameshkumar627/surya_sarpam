# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave Application
PROGRESS_INFO = [('draft', 'draft'), ('approved', 'Approved')]


class LeaveConfiguration(surya.Sarpam):
    _name = "leave.configuration"

    level_id = fields.Many2one(comodel_name="leave.level", string="Level", required=True)
    leave_configuration_detail = fields.One2many(comodel_name="leave.configuration.detail",
                                                 inverse_name="configuration_id",
                                                 string="Leave Configuration Detail")


class LeaveConfigurationDetail(surya.Sarpam):
    _name = "leave.configuration.detail"

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    order = fields.Integer(string="Order Sequence")
    increment = fields.Float(string="Increment", required=True)
    configuration_id = fields.Many2one(comodel_name="leave.configuration",
                                       string="Leave Configuration")


class LeaveLevel(surya.Sarpam):
    _name = "leave.level"

    name = fields.Char(string="Level", required=True)


class LeaveType(surya.Sarpam):
    _name = "leave.type"

    name = fields.Char(string="Type", required=True)
