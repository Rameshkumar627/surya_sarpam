# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Year Configuration

class Year(surya.Sarpam):
    _name = "year.year"

    name = fields.Char(string="Year", required=True)
    previous_year = fields.Many2one(comodel_name="year.year", string="Previous Year")
    next_year = fields.Many2one(comodel_name="year.year", string="Next Year")
    year_detail = fields.One2many(comodel_name="year.year",
                                  inverse_name="year_id",
                                  string="Month")


class Month(surya.Sarpam):
    _name = "month.month"

    name = fields.Char(string="Month", required=True)
    day_detail = fields.One2many(comodel_name="day.day", inverse_name="month_id", string="Day")
    next_month = fields.Many2one(comodel_name="month.month", string="Next Month")
    previous_month = fields.Many2one(comodel_name="month.month", string="Previous Month")
    year_id = fields.Many2one(comodel_name="year.year", string="Year")


class Week(surya.Sarpam):
    _name = "week.week"

    name = fields.Char(string="Week", required=True)
    next_week = fields.Many2one(comodel_name="week.week", string="Next Week")
    previous_week = fields.Many2one(comodel_name="week.week", string="Previous Week")
    day_detail = fields.One2many(comodel_name="day.day",
                                 inverse_name="week_id",
                                 string="Day")


class Day(surya.Sarpam):
    _name = "day.day"

    name = fields.Char(string="Date", required=True)
    next_day = fields.Many2one(comodel_name="day.day", string="Next Day")
    previous_day = fields.Many2one(comodel_name="day.day", string="Previous Day")
    week_id = fields.Many2one(comodel_name="week.week", string="Week")
    month_id = fields.Many2one(comodel_name="month.month", string="Month")