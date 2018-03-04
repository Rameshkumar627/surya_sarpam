# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from xlwt import *
import base64

try:
    import xlwt
except:
    raise exceptions.ValidationError('Warning ! python-xlwt module missing. Please install it.')


REPORT_TYPE = [('html', 'HTML'), ('pdf', 'PDF'), ('excel', 'Excel')]

from odoo import http
from odoo.http import request



class Example(http.Controller):
    @http.route('/example', type='http', auth='public', website=True)
    def render_example_page(self):
        print request.env["report.report"].search([])
        return "tt"


class Report(surya.Sarpam):
    _name = "report.report"

    name = fields.Char(string="Name")
    others = fields.Char(string="Others")

    report_type = fields.Selection(selection=REPORT_TYPE, string="Report Type")

    column_detail = fields.One2many(comodel_name="report.column",
                                    inverse_name="report_id",
                                    string="Data Field")
    report_design = fields.One2many(comodel_name="report.design",
                                    inverse_name="report_id",
                                    string="Report Design")
    model = fields.Many2one(comodel_name="ir.model", string="Model")

    filename = fields.Char(string="File name")
    file_output = fields.Binary(string="File Output")
    maxtor = fields.Many2many(comodel_name="ir.attachment")

    def query_creation(self):
        model_list = []
        field_name = []
        for rec in self.column_detail:
            model = rec.model.model.replace(".", "_")
            field_data = rec.data_field.name.replace(".", "_")
            field_name.append('"{0}"."{1}"'.format(model, field_data))
            if model not in model_list:
                model_list.append(model)

            relation = rec.data_field.relation.replace(".", "_")




        query = "select {0} from {1}".format(",".join(field_name), ",".join(model_list))


        return query

    def row_creation_above(self, sheet1):
        recs = self.env["report.design"].search([("report_id", "=", self.id),
                                                 ("row_type", "=", "above")])

        recs.sorted(key=lambda r: r.order_seq)

        for rec in recs:
            style = xlwt.easyxf(rec.style_id.style)
            sheet1.write_merge(rec.row_1, rec.row_2, rec.col_1, rec.col_2, rec.data, style)

        return sheet1

    def row_creation_footer(self, sheet1, row, vals):
        rec = self.env["report.design"].search([("report_id", "=", self.id),
                                                ("row_type", "=", "footer")])

        row = row + 1

        columns = self.env["report.column"].search([("column_seq", ">", 0), ("sum_footer", "=", True)])
        style = xlwt.easyxf(rec.style_id.style)

        for column in columns:
            data = 0
            for val in vals:
                data = data + val[column.column_seq - 1]

            sheet1.write(row, column.column_seq, float(data), style)

        return sheet1, row

    def header_creation(self, sheet1):
        rec = self.env["report.design"].search([("report_id", "=", self.id),
                                                ("row_type", "=", "header")])

        row = rec.start_row

        columns = self.env["report.column"].search([("column_seq", ">", 0)])
        style = xlwt.easyxf(rec.style_id.style)

        for column in columns:
            sheet1.write(row, column.column_seq, column.name, style)

        return sheet1, row

    def body_creation(self, sheet1, row, datas):
        rec = self.env["report.design"].search([("report_id", "=", self.id),
                                                ("row_type", "=", "body")])

        columns = self.env["report.column"].search([("column_seq", ">", 0)])
        style = xlwt.easyxf(rec.style_id.style)

        for data in datas:
            row = row + 1
            for column in columns:
                sheet1.write(row, column.column_seq, data[column.column_seq - 1], style)

        return sheet1, row

    def file_creation(self, path):
        encoded_string = ""
        with open('{0}/{1}.xls'.format(path, self.id), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        self.filename = 'Store Request.xls'
        self.file_output = encoded_string

    @api.multi
    def trigger_field_data(self):
        book = xlwt.Workbook()

        sheet1 = book.add_sheet('Store Request')
        sheet1 = self.row_creation_above(sheet1)
        sheet1, row = self.header_creation(sheet1)

        query = self.query_creation()

        print query
        self._cr.execute(query)
        vals = self._cr.fetchall()

        sheet1, row = self.body_creation(sheet1, row, vals)
        sheet1 = self.row_creation_footer(sheet1, row, vals)

        path = "/home/sarpam/Desktop"
        book.save('{0}/{1}.xls'.format(path, self.id))
        self.file_creation(path)


class ReportColumn(surya.Sarpam):
    _name = "report.column"

    name = fields.Char(string="Name")
    model = fields.Many2one(comodel_name="ir.model", string="Model")
    data_field = fields.Many2one(comodel_name="ir.model.fields",
                                 string="Fields",
                                 domain="[('model_id', '=', model)]")
    column_seq = fields.Integer(string="Column")
    sum_footer = fields.Boolean(string="Sum")
    report_id = fields.Many2one(comodel_name="report.report", string="Report")


class ReportDesign(surya.Sarpam):
    _name = "report.design"

    row_1 = fields.Integer(string="Row 1")
    col_1 = fields.Integer(string="Col 1")
    row_2 = fields.Integer(string="Row 2")
    col_2 = fields.Integer(string="Col 2")
    template = fields.Text(string="Template")
    row_type = fields.Selection(selection=[("above", 'Above'),
                                           ("header", "Header"),
                                           ("body", "Body"),
                                           ("footer", "Footer"),
                                           ("below", "Below")])
    start_row = fields.Integer(string="Start Row")
    style_id = fields.Many2one(comodel_name="style.detail", string="Style")
    order_seq = fields.Integer(string="Order")
    data = fields.Char(string="Data")

    report_id = fields.Many2one(comodel_name="report.report", string="Report")


class StyleDetail(surya.Sarpam):
    _name = "style.detail"

    style = fields.Text(string="Style")
    type = fields.Selection(selection=[("css", "CSS"), ("excel", "Excel")])


