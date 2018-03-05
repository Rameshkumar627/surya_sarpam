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
    _rec_name = "sequence"

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
    comment = fields.Text(string='Comment')

    total = fields.Float(string='Total', readonly=True)
    freight_amount = fields.Float(string="Freight Amount")
    discount_amount = fields.Float(string='Discount Amount', readonly=True, help='Discount value')
    discounted_amount = fields.Float(string='Discounted Amount', readonly=True, help='Amount after discount')
    tax_amount = fields.Float(string='Tax Amount', readonly=True, help='Tax value')
    taxed_amount = fields.Float(string='Taxed Amount', readonly=True, help='Tax after discounted amount')
    un_taxed_amount = fields.Float(string='Untaxed Amount', readonly=True)
    sgst = fields.Float(string='SGST', readonly=True)
    cgst = fields.Float(string='CGST', readonly=True)
    igst = fields.Float(string='IGST', readonly=True)
    gross_amount = fields.Float(string='Gross Amount', readonly=True)
    round_off = fields.Float(string='Round-Off', readonly=True)
    net_amount = fields.Float(string='Net Amount', readonly=True)

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
                                         "quantity": rec.accepted_quantity,
                                         "unit_price": rec.unit_price,
                                         "discount": rec.discount,
                                         "tax_id": rec.tax_id.id}))

        data = {"indent_id": self.indent_id.id,
                "vendor_id": self.vendor_id.id,
                "vs_id": self.vs_id.id,
                "quotation_id": self.id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "po_detail": po_detail}

        if (count > 0) and (self.progress == 'draft'):
            self.env["purchase.order"].create(data)

        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        self.write({"progress": "po_generated",
                    "processed_by": employee_id.id,
                    "processed_on": datetime.now().strftime("%Y-%m-%d")})

    @api.multi
    def trigger_update(self):
        recs = self.quotation_detail

        total = freight_amount = 0
        discount_amount = discounted_amount = 0
        tax_amount = taxed_amount = un_taxed_amount = 0
        cgst = sgst = igst = 0
        gross_amount = round_off = net_amount = 0

        for rec in recs:
            rec.calculate_total()

            total = total + rec.total
            discount_amount = discount_amount + rec.discount_amount
            discounted_amount = discounted_amount + rec.discounted_amount
            tax_amount = tax_amount + rec.tax_amount
            taxed_amount = taxed_amount + rec.taxed_amount
            un_taxed_amount = un_taxed_amount + rec.un_taxed_amount
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst

        freight_amount = self.freight_amount
        un_taxed_amount = un_taxed_amount + self.freight_amount
        gross_amount = total + freight_amount
        net_amount = round(gross_amount)
        round_off = net_amount - gross_amount

        data = {"total": total,
                "freight_amount": freight_amount,
                "discount_amount": discount_amount,
                "discounted_amount": discounted_amount,
                "tax_amount": tax_amount,
                "taxed_amount": taxed_amount,
                "un_taxed_amount": un_taxed_amount,
                "sgst": sgst,
                "cgst": cgst,
                "igst": igst,
                "gross_amount": gross_amount,
                "round_off": round_off,
                "net_amount": net_amount}

        self.write(data)

