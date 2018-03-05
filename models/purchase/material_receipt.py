# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('received', 'Received'),
                 ('inspected', 'Inspected')]


class MaterialReceipt(surya.Sarpam):
    _name = "material.receipt"
    _rec_name = "sequence"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    po_id = fields.Many2one(comodel_name="purchase.order",
                            string="Purchase Order",
                            domain="[('progress', '=', 'approved')]",
                            readonly=True)
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    vs_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection', readonly=True)
    processed_by = fields.Many2one(comodel_name='hr.employee', string='Processed By', readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    mr_detail = fields.One2many(comodel_name='mr.detail', inverse_name='mr_id',
                                string='Material Receipt Detail')
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
    def trigger_update(self):
        recs = self.mr_detail

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

    def check_previous_mr(self):
        recs = self.mr_detail

        for rec in recs:
            qty = 0
            mrs = self.env["mr.detail"].search([("product_id", "=", rec.product_id.id),
                                                ("mr_id.indent_id", "=", self.indent_id.id)])

            for mr in mrs:
                qty = qty + mrs.accepted_quantity

            indent = self.env["indent.detail"].search([("product_id", "=", rec.product_id.id),
                                                       ("id", "=", self.indent_id.id)])
            if qty > indent.quantity:
                raise exceptions.ValidationError("Error! material receipt is more than indent raised")

    def stock_updation(self):
        recs = self.mr_detail

        for rec in recs:
            rec.stock_updation()

    @api.multi
    def trigger_inspected(self):
        self.check_previous_mr()
        self.stock_updation()
        self.write({"progress": "inspected"})

    @api.multi
    def trigger_received(self):
        self.write({"progress": "received"})


class MRDetail(surya.Sarpam):
    _name = "mr.detail"

    product_id = fields.Many2one(comodel_name='product.product', string='Product', readonly=True)
    uom_id = fields.Many2one(comodel_name='product.uom', string='UOM', readonly=True)
    requested_quantity = fields.Float(string='Requested Quantity', readonly=True)
    received_quantity = fields.Float(string="Received Quantity")
    accepted_quantity = fields.Float(string="Accepted Quantity")
    unit_price = fields.Float(string='Unit Price', default=0, readonly=True)
    discount = fields.Float(string='Discount', default=0, readonly=True)
    discount_amount = fields.Float(string='Discount Amount', default=0, readonly=True)
    discounted_amount = fields.Float(string='Discounted Amount', default=0, readonly=True)
    tax_id = fields.Many2one(comodel_name='product.tax', string='Tax', readonly=True)
    igst = fields.Float(string='IGST', default=0, readonly=True)
    cgst = fields.Float(string='CGST', default=0, readonly=True)
    sgst = fields.Float(string='SGST', default=0, readonly=True)
    tax_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', default=0, readonly=True)
    un_taxed_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    total = fields.Float(string='Total', default=0, readonly=True)
    mr_id = fields.Many2one(comodel_name='material.receipt', string='Material Receipt')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='mr_id.progress')

    def stock_updation(self):
        product_conf = self.env["product.configuration"].search([])
        self.env["stock.move"].create({"product_id": self.product_id.id,
                                       "quantity": self.accepted_quantity,
                                       "destination_id": product_conf.default_location_id.id,
                                       "progress": "in"})

    @api.multi
    def calculate_total(self):
        price = self.accepted_quantity * self.unit_price

        pc_obj = PC()
        discount_amount = pc_obj.calculate_percentage(price, self.discount)

        discounted_amount = price - discount_amount
        igst, cgst, sgst = pc_obj.calculate_tax(discounted_amount, self.tax_id.value, self.tax_id.name)
        tax_amount = igst + cgst + sgst
        total = discounted_amount + tax_amount

        data = {'discount_amount': discount_amount,
                'discounted_amount': discounted_amount,
                'igst': igst,
                'cgst': cgst,
                'sgst': sgst,
                'tax_amount': tax_amount,
                'taxed_amount': total,
                'un_taxed_amount': 0,
                'total': total
                }

        self.write(data)

    @api.constrains('received_quantity')
    def _validate_received_quantity(self):
        message = "Error! Received quantity is greater than Requested quantity"
        if self.received_quantity > self.requested_quantity:
            raise exceptions.ValidationError(message)

    @api.constrains('accepted_quantity')
    def _validate_accepted_quantity(self):
        message = "Error! Accepted quantity is greater than Received quantity"
        if self.accepted_quantity > self.received_quantity:
            raise exceptions.ValidationError(message)
