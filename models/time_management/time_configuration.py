# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, date, timedelta
from .. import surya
import json


# Time Configuration


class TimeConfiguration(surya.Sarpam):
    _name = "time.configuration"

    time_delay = fields.Float(string="Time Delay")
