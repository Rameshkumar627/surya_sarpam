# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

# Time Sheet


class TimeMachine(surya.Sarpam):
    _name = "time.machine"

    name = fields.Char(string="Name")

    def attendance_calc(self, status):
        conf = self.env["time.configuration"].search([("id", "=", 1)])
        time_delay = conf.time_delay

        current_time = datetime.now()
        fmt = "%Y-%m-%d %H:%M:%S"

        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        date = current_time.strftime("%Y-%m-%d")
        data = {"date": date,
                "employee_id": employee_id.id,
                "progress": status}

        rec = self.env["time.sheet"].create(data)

        attendances = self.env["attendance.detail"].search([("employee_id", "=", employee_id.id),
                                                            ("attendance_id.date", ">=", date)])

        for atten in attendances:
            date = atten.attendance_id.date
            end_day = atten.shift.end_day

            start_hrs = atten.shift.from_time // 1
            start_min = ((atten.shift.from_time % 1) * 60) / 100

            end_hrs = atten.shift.till_time // 1
            end_min = ((atten.shift.till_time % 1) * 60) / 100

            start_time = datetime.strptime("{0} {1}:{2}:00".format(date, int(start_hrs), int(start_min)), fmt)
            start_time = start_time - timedelta(minutes=time_delay)

            if end_day == 'current_day':
                end_time = datetime.strptime("{0} {1}:{2}:00".format(date, int(end_hrs), int(end_min)), fmt)
            elif end_day == 'next_day':
                end_date = ((datetime.strptime(date, "%Y-%m-%d")) + timedelta(days=1)).strftime("%Y-%m-%d")
                end_time = datetime.strptime("{0} {1}:{2}:00".format(end_date, int(end_hrs), int(end_min)), fmt)

            end_time = end_time + timedelta(minutes=time_delay)

            if end_time > current_time > start_time:
                print atten.id
                actual_hrs = datetime.now().strftime("%H")
                actual_min = datetime.now().strftime("%M")

                actual = float(actual_hrs) + (float(actual_min) / 60)

                if status == "in":
                    atten.write({"actual_in": actual + 5.50})
                elif status == "out":
                    atten.write({"actual_out": actual + 5.50})

    def trigger_in(self):
        self.attendance_calc(status="in")

    def trigger_out(self):
        self.attendance_calc(status="out")
