# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Purchase Order
PROGRESS_INFO = [('draft', 'Draft'),
                 ('approved', 'Approved'),
                 ('partially_received', 'Partially Received'),
                 ('fully_received', 'Fully Received'),
                 ('cancelled', 'Cancelled')]


class PurchaseOrder(surya.Sarpam):
    _name = "purchase.order"

    sequence = fields.Char(string="Sequence", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    date = fields.Date(string="Date")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor")
    vs_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection', readonly=True)
    quotation_id = fields.Many2one(comodel_name='purchase.quotation', string='Quotation', readonly=True)

    processed_by = fields.Many2one(comodel_name='hr.employee', string='Processed By', readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    po_detail = fields.One2many(comodel_name='po.detail', inverse_name='po_id',
                                string='Purchase Order Detail')
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
    def trigger_update(self):
        recs = self.po_detail

        for rec in recs:
            rec.calculate_total()

    @api.multi
    def trigger_approved(self):
        self.write({"progress": "approved"})


class PurchaseOrderDetail(surya.Sarpam):
    _name = "po.detail"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    cgst = fields.Float(string="CGST")
    igst = fields.Float(string="IGST")
    sgst = fields.Float(string="SGST")
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax")
    tax_amount = fields.Float(string="Tax Amount")
    discount = fields.Float(string="Discount")
    discounted_amount = fields.Float(string="Discounted Amount")
    total = fields.Float(string="Total")
    po_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")

    @api.multi
    def calculate_total(self):
        price = self.quantity * self.unit_price

        pc_obj = PC()
        discount_amount = pc_obj.calculate_percentage(price, self.discount)

        amt_after_discount = price - discount_amount
        igst, cgst, sgst = pc_obj.calculate_tax(amt_after_discount, self.tax_id.value, self.tax_id.name)
        tax_amount = igst + cgst + sgst
        total = amt_after_discount + tax_amount

        data = {'discount_amount': discount_amount,
                'amt_after_discount': amt_after_discount,
                'igst': igst,
                'cgst': cgst,
                'sgst': sgst,
                'tax_amount': tax_amount,
                'taxed_amount': 0,
                'un_taxed_amount': 0,
                'total': total
                }

        self.write(data)
