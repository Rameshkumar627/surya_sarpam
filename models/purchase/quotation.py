# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('po_generated', 'PO Generated'),
                 ('cancelled', 'Cancelled')]


class Quotation(surya.Sarpam):
    _name = "purchase.quotation"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string="Date")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    vs_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection', readonly=True)
    vendor_ref = fields.Char(string='Vendor Ref')
    processed_by = fields.Many2one(comodel_name='hr.employee', string='Processed By', readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    quotation_detail = fields.One2many(comodel_name='vs.quote.detail', inverse_name='quotation_id', string='Quotation Detail')
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    grand_total = fields.Float(string='Grand Total', readonly=True)
    overall_discount = fields.Float(string='Overall Discount', default=0)
    discount_amount = fields.Float(string='Discount Amount', readonly=True)
    igst = fields.Float(string='IGST', readonly=True)
    cgst = fields.Float(string='CGST', readonly=True)
    sgst = fields.Float(string='SGST', readonly=True)
    tax_amount = fields.Float(string='Tax Amount', readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', readonly=True)
    un_taxed_amount = fields.Float(string='Untaxed Amount', readonly=True)
    gross_amount = fields.Float(string='Gross Amount', readonly=True)
    round_off = fields.Float(string='Round-Off', readonly=True)
    net_amount = fields.Float(string='Net Amount', readonly=True)
    comment = fields.Text(string='Comment')

    @api.multi
    def trigger_quote_approve(self):
        count = 0
        po_detail = []
        recs = self.quotation_detail

        for rec in recs:
            if rec.accepted_quantity:
                count = count + 1
                po_detail.append((0, 0, {"product_id": rec.product_id.id,
                                         "uom_id": rec.uom_id.id,
                                         "unit_price": rec.unit_price,
                                         "quantity": rec.accepted_quantity,
                                         "cgst": rec.cgst,
                                         "igst": rec.igst,
                                         "sgst": rec.sgst,
                                         "tax_id": rec.tax_id.id,
                                         "discount": rec.discount}))

        data = {"indent_id": self.indent_id.id,
                "vendor_id": self.vendor_id.id,
                "vs_id": self.vs_id.id,
                "quotation_id": self.id,
                "po_detail": po_detail
                }

        if (count > 0) and (self.progress == 'draft'):
            self.env["purchase.order"].create(data)

        self.write({"progress": "po_generated"})

    @api.multi
    def trigger_update(self):
        recs = self.quotation_detail

        for rec in recs:
            rec.calculate_total()

        data = {""}

