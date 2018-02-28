# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class MatProcess(surya.Sarpam):
    _name = "mat.process"