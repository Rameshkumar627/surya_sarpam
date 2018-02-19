# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from collections import OrderedDict
import calendar
from . import surya
import json


# Year Configuration


class Year(surya.Sarpam):
    _name = "year.year"
    _rec_name = 'name'

    name = fields.Char(string="Year", required=True)
    previous_year = fields.Many2one(comodel_name="year.year", string="Previous Year", readonly=True)
    next_year = fields.Many2one(comodel_name="year.year", string="Next Year", readonly=True)
    month_detail = fields.One2many(comodel_name="month.month", inverse_name="year_id", string="Month", readonly=True)
    year_int = fields.Integer(string="Year Int")

    def default_vals_creation(self, vals):
        vals["year_int"] = int(vals['name'])
        return vals

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    @api.multi
    def trigger_year_update(self):
        start_date = datetime.strptime('{0}-01-01'.format(self.year_int), '%Y-%m-%d')
        end_date = datetime.strptime('{0}-01-01'.format(self.year_int + 1), '%Y-%m-%d')

        month = week = None
        month_id = week_id = None

        day = 0

        for single_date in self.daterange(start_date, end_date):
            day = day + 1
            if single_date.strftime("%m") != month:
                month_id = self.env["month.month"].create({"name": single_date.strftime("%m-%Y"),
                                                           "month_int": int(single_date.strftime("%m")),
                                                           "year_id": self.id})
                month = single_date.strftime("%m")

            if single_date.strftime("%U") != week:
                week_check = self.env["week.week"].search([("name", "=", single_date.strftime("%U-%Y"))])
                if not week_check:
                    week_id = self.env["week.week"].create({"name": single_date.strftime("%U-%Y"),
                                                            "week_int": int(single_date.strftime("%U")),
                                                            "year_id": self.id})
                else:
                    week_id = week_check
                week = single_date.strftime("%U")

            self.env["day.day"].create({"name": single_date.strftime("%Y-%m-%d"),
                                        "day_int": day,
                                        "month_id": month_id.id,
                                        "week_id": week_id.id,
                                        "year_id": self.id})

        month_recs = self.env["month.month"].search([("year_id", "=", self.id)])
        for rec in month_recs:
            rec.month_previous_next()
        week_recs = self.env["week.week"].search([("year_id", "=", self.id)])
        for rec in week_recs:
            rec.week_previous_next()
        day_recs = self.env["day.day"].search([("year_id", "=", self.id)])
        for rec in day_recs:
            rec.day_previous_next()

        previous_year = self.env["year.year"].search([("year_int", "=", self.year_int - 1)])
        next_year = self.env["year.year"].search([("year_int", "=", self.year_int + 1)])

        data = {}

        if previous_year:
            data["previous_year"] = previous_year.id
        if next_year:
            data["next_year"] = next_year.id

        self.write(data)

    _sql_constraints = [('unique_year', 'unique (name)', 'Error! Year should not be repeated')]


class Month(surya.Sarpam):
    _name = "month.month"
    _rec_name = 'name'

    name = fields.Char(string="Month", readonly=True)
    previous_month = fields.Many2one(comodel_name="month.month", string="Previous Month", readonly=True)
    next_month = fields.Many2one(comodel_name="month.month", string="Next Month", readonly=True)
    year_id = fields.Many2one(comodel_name="year.year", string="Year", readonly=True)
    day_detail = fields.One2many(comodel_name="day.day", inverse_name="month_id", string="Day", readonly=True)
    month_int = fields.Integer(string="Month Int")

    def month_previous_next(self):
        previous_month = self.env["month.month"].search([("year_id", "=", self.year_id.id),
                                                         ("month_int", "=", self.month_int - 1 )])
        next_month = self.env["month.month"].search([("year_id", "=", self.year_id.id),
                                                     ("month_int", "=", self.month_int + 1 )])

        data = {}

        if previous_month:
            data["previous_month"] = previous_month.id
        if next_month:
            data["next_month"] = next_month.id

        self.write(data)

    _sql_constraints = [('unique_month', 'unique (name)', 'Error! Month should not be repeated')]


class Week(surya.Sarpam):
    _name = "week.week"
    _rec_name = 'name'

    name = fields.Char(string="Week", required=True)
    previous_week = fields.Many2one(comodel_name="week.week", string="Previous Week")
    next_week = fields.Many2one(comodel_name="week.week", string="Next Week")
    year_id = fields.Many2one(comodel_name="year.year", string="Year")
    day_detail = fields.One2many(comodel_name="day.day",
                                 inverse_name="week_id",
                                 string="Day")
    week_int = fields.Integer(string="Week Int")

    def week_previous_next(self):
        previous_week = self.env["week.week"].search([("year_id", "=", self.year_id.id),
                                                      ("week_int", "=", self.week_int - 1)])
        next_week = self.env["week.week"].search([("year_id", "=", self.year_id.id),
                                                  ("week_int", "=", self.week_int + 1)])

        data = {}

        if previous_week:
            data["previous_week"] = previous_week.id
        if next_week:
            data["next_week"] = next_week.id

        self.write(data)

    _sql_constraints = [('unique_week', 'unique (name)', 'Error! Week should not be repeated')]


class Day(surya.Sarpam):
    _name = "day.day"
    _rec_name = 'name'

    name = fields.Char(string="Date", required=True)
    previous_day = fields.Many2one(comodel_name="day.day", string="Previous Day")
    next_day = fields.Many2one(comodel_name="day.day", string="Next Day")
    week_id = fields.Many2one(comodel_name="week.week", string="Week")
    month_id = fields.Many2one(comodel_name="month.month", string="Month")
    year_id = fields.Many2one(comodel_name="year.year", string="Year")
    day_int = fields.Integer(string="Day Int")

    def day_previous_next(self):
        previous_day = self.env["day.day"].search([("year_id", "=", self.year_id.id),
                                                   ("day_int", "=", self.day_int - 1)])
        next_day = self.env["day.day"].search([("year_id", "=", self.year_id.id),
                                               ("day_int", "=", self.day_int + 1)])

        data = {}

        if previous_day:
            data["previous_day"] = previous_day.id
        if next_day:
            data["next_day"] = next_day.id

        self.write(data)

    _sql_constraints = [('unique_day', 'unique (name)', 'Error! Day should not be repeated')]