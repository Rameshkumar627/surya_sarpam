# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


PROGRESS_INFO = [('draft', 'Draft'),
                 ('qa', 'Quotation Approved'),
                 ('cancel', 'Cancel')]


class VSQuoteDetail(surya.Sarpam):
    _name = 'vs.quote.detail'
    _description = 'Vendor Selection Quote Detail'

    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', readonly=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', related='vs_quote_id.product_id')
    uom_id = fields.Many2one(comodel_name='product.uom', string='UOM', related='vs_quote_id.uom_id')
    requested_quantity = fields.Float(string='Requested Quantity', default=0)
    accepted_quantity = fields.Float(string='Accepted Quantity', default=0)
    unit_price = fields.Float(string='Unit Price', default=0)
    discount = fields.Float(string='Discount', default=0, readonly=True)
    discount_amount = fields.Float(string='Discount Amount', default=0, readonly=True)
    amt_after_discount = fields.Float(string='Discount Amount', default=0, readonly=True)
    tax_id = fields.Many2one(comodel_name='product.tax', string='Tax')
    igst = fields.Float(string='IGST', default=0, readonly=True)
    cgst = fields.Float(string='CGST', default=0, readonly=True)
    sgst = fields.Float(string='SGST', default=0, readonly=True)
    tax_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', default=0, readonly=True)
    un_taxed_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    total = fields.Float(string='Total', default=0, readonly=True)
    vs_quote_id = fields.Many2one(comodel_name='vs.detail', string='Vendor Selection')
    quotation_id = fields.Many2one(comodel_name='purchase.quotation', string='Quotation')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='quotation_id.progress')

    @api.multi
    def calculate_total(self):
        price = self.accepted_quantity * self.unit_price

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

