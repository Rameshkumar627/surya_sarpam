# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Vendor Selection
PROGRESS_INFO = [('draft', 'Draft'),
                 ('qa', 'Quotation Approved'),
                 ('cancelled', 'Cancelled')]


class VendorSelection(surya.Sarpam):
    _name = "vendor.selection"

    date = fields.Date(string='Date', readonly=True)
    indent_id = fields.Many2one(comodel_name='purchase.indent',
                                string='Purchase Indent',
                                required=True)
    quote_comparision = fields.Binary(string="Quote Comparision")
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    selection_detail = fields.One2many(comodel_name='vs.detail',
                                       inverse_name='selection_id', string='Vendor Selection Details')
    comment = fields.Text(string='Comment')

    def default_vals_creation(self, vals):
        vals['date'] = datetime.now().strftime("%Y-%m-%d")
        selection_detail = []

        indent = self.env["purchase.indent"].search([("id", "=", vals['indent_id'])])
        recs = indent.indent_detail

        for rec in recs:
            selection_detail.append((0, 0, {

                "product_id": rec.product_id.id,
                "uom_id": rec.uom_id.id,
                "quantity": rec.quantity
            }))

        vals['selection_detail'] = selection_detail

        return vals

    @api.multi
    def trigger_quote_creation(self):
        recs = self.selection_detail

        for rec in recs:
            rec.quote_detail_creation()

    @api.multi
    def trigger_quotes_approved(self):
        recs = self.env["purchase.quotation"].search([("vs_id", "=", self.id)])

        for rec in recs:
            rec.trigger_quote_approve()

        self.write({"progress": "qa"})

    @api.multi
    def trigger_quotes_cancel(self):
        recs = self.env["purchase.quotation"].search([("vs_id", "=", self.id)])

        for rec in recs:
            rec.write({"progress": "cancelled"})

        self.write({"progress": "cancelled"})


class VSDetail(surya.Sarpam):
    _name = 'vs.detail'
    _description = 'Vendor Selection Details'

    product_id = fields.Many2one(comodel_name='product.product', string='Product', readonly=True)
    uom_id = fields.Many2one(comodel_name='product.uom', string='UOM', readonly=True)
    quantity = fields.Float(string='Quantity', readonly=True)

    vendor_ids = fields.Many2many(comodel_name='res.partner', string='Vendors')
    quote_detail = fields.One2many(comodel_name='vs.quote.detail', inverse_name='vs_quote_id',
                                   string='Quote Detail')
    comment = fields.Text(string='Comment')
    selection_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='selection_id.progress')

    @api.multi
    def quote_detail_creation(self):
        for vendor in self.vendor_ids:
            quote = self.env["purchase.quotation"].search([("indent_id", "=", self.selection_id.indent_id.id),
                                                           ("vendor_id", "=", vendor.id),
                                                           ("vs_id", "=", "self.id"),
                                                           ("progress", "=", "draft")])

            if quote:
                quote_detail = self.env["vs.quote.detail"].search([("product_id", "=", self.product_id.id),
                                                                   ("uom_id", "=", self.uom_id.id),
                                                                   ("quotation_id", "=", quote.id)])

                if not quote_detail:
                    self.env["vs.quote.detail"].create({"vendor_id": vendor.id,
                                                        "product_id": self.product_id.id,
                                                        "uom_id": self.uom_id.id,
                                                        "requested_quantity": self.quantity,
                                                        "vs_quote_id": self.id,
                                                        "quotation_id": quote.id})

            else:
                quotation_detail = [(0, 0, {"vendor_id": vendor.id,
                                            "product_id": self.product_id.id,
                                            "uom_id": self.uom_id.id,
                                            "vs_quote_id": self.id,
                                            "requested_quantity": self.quantity})]

                data = {"indent_id": self.selection_id.indent_id.id,
                        "vendor_id": vendor.id,
                        "vs_id": self.selection_id.id,
                        "quotation_detail": quotation_detail}

                self.env["purchase.quotation"].create(data)




