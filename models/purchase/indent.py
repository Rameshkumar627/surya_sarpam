# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('wfa', 'Waiting For Approval'),
                 ('approved', 'Approved'),
                 ('closed', 'Closed'),
                 ('cancelled', 'Cancelled')]


class PurchaseIndent(surya.Sarpam):
    _name = "purchase.indent"
    _rec_name = "sequence"

    def _get_indent_detail(self):
        detail = []

        if self._context.get("active_model") == "low.stock":
            ids = self._context.get("active_ids")

            recs = self.env["low.stock"].search([("id", "in", ids)])

            for rec in recs:
                detail.append((0, 0, {"product_id": rec.product_id.id,
                                      "uom_id": rec.uom_id.id,
                                      "quantity": rec.quantity,
                                      "progress": "draft"}))

        return detail

    sequence = fields.Char(string="Sequence", readonly=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', readonly=True)
    requested_by = fields.Many2one(comodel_name='hr.employee', string='Requested By', readonly=True)
    requested_on = fields.Date(string='Requested On', readonly=True)
    approved_by = fields.Many2one(comodel_name='hr.employee', string='Approved By', readonly=True)
    approved_on = fields.Date(string='Approved On', readonly=True)
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    indent_detail = fields.One2many(comodel_name='indent.detail',
                                    string='Purchase Indent Detail',
                                    default=_get_indent_detail,
                                    inverse_name='indent_id')
    comment = fields.Text(string='Comment')

    def default_vals_creation(self, vals):
        vals['requested_on'] = datetime.now().strftime("%Y-%m-%d")
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals['requested_by'] = employee_id.id
        vals['employee_id'] = employee_id.id
        vals['department_id'] = employee_id.department_id.id

        return vals

    @api.multi
    def trigger_wfa(self):
        recs = self.indent_detail

        for rec in recs:
            rec.low_stock_clearance()

        data = {'sequence': self.env['ir.sequence'].sudo().next_by_code('purchase.indent'),
                'progress': 'wfa'}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        data = {'approved_on': datetime.now().strftime("%Y-%m-%d"),
                'approved_by': employee_id.id,
                'progress': 'approved'}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        data = {'approved_on': datetime.now().strftime("%Y-%m-%d"),
                'approved_by': employee_id.id,
                'progress': 'cancelled'}

        self.write(data)

    @api.multi
    def trigger_closed(self):
        vs = self.env["vendor.selection"].search([("indent_id", "=", self.id), ("progress", "in", ["draft"])])
        if vs:
            raise exceptions.ValidationError("Error! You cannot close this indent Vendor Selection is in progress")

        quote = self.env["purchase.quotation"].search([("indent_id", "=", self.id), ("progress", "in", ["draft"])])
        if quote:
            raise exceptions.ValidationError("Error! You cannot close this indent quotation is in progress")

        po = self.env["purchase.order"].search([("indent_id", "=", self.id), ("progress", "in", ["draft"])])
        if po:
            raise exceptions.ValidationError("Error! You cannot close this indent Purchase Order is in progress")

        mr = self.env["material.receipt"].search([("indent_id", "=", self.id), ("progress", "in", ["draft", "received"])])
        if mr:
            raise exceptions.ValidationError("Error! You cannot close this indent Material Receipt is in progress")

        data = {'progress': 'closed'}

        self.write(data)


class IndentDetail(surya.Sarpam):
    _name = "indent.detail"

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    comment = fields.Text(string="Comment")
    indent_id = fields.Many2one(comodel_name='purchase.indent', string='Purchase Indent')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='indent_id.progress')

    _sql_constraints = [('unique_indent_detail', 'unique (product_id, indent_id)', 'Error! Week should not be repeated')]

    def low_stock_clearance(self):
        low_stock = self.env["low.stock"].search([("product_id", "=", self.product_id.id),
                                                  ("uom_id", "=", self.uom_id.id)])
        if low_stock:
            low_stock.write({"progress": "indent_raised"})
