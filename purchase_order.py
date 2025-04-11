from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_filter = fields.Boolean(string="Enable Vendor Product Filter")

    @api.onchange('partner_id')
    def _onchange_partner_id_add_products(self):
        if self.partner_id:
            # Clear existing order lines
            self.order_line = [(5, 0, 0)]

            # Find all products with this vendor
            products = self.env['product.product'].search([
                ('seller_ids.partner_id', '=', self.partner_id.id)
            ])

            lines = []
            for product in products:
                lines.append((0, 0, {
                    'product_id': product.id,
                    'name': product.name,
                    'product_qty': 1.0,
                    'product_uom': product.uom_po_id.id,
                    'price_unit': product.standard_price,
                    'date_planned': fields.Date.today(),
                }))

            self.order_line = lines

# models/purchase_order_line.py
from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sales_price = fields.Float(string="Sales Price")

# from odoo import models, fields, api
#
# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#
#     vendor_filter = fields.Boolean(string="Vendor Filter")
#     vendor_product_ids = fields.Many2many(
#         "product.product", compute="_compute_vendor_products", string="Vendor Products"
#     )
#
#     @api.depends('partner_id')
#     def _compute_vendor_products(self):
#         """ Fetch products associated with the selected vendor """
#         for order in self:
#             if not order.partner_id:
#                 order.vendor_product_ids = [(5, 0, 0)]  # Clear the field
#                 continue
#
#             supplier_info = self.env['product.supplierinfo'].search([
#                 ('partner_id', '=', order.partner_id.id)  # Use 'partner_id' instead of 'name'
#             ])
#             order.vendor_product_ids = supplier_info.mapped('product_tmpl_id.product_variant_ids')
#
#     @api.onchange('vendor_filter')
#     def _onchange_vendor_filter(self):
#         """ Add vendor's products to purchase order lines when vendor_filter is True """
#         for order in self:
#             if order.vendor_filter and order.vendor_product_ids:
#                 order.order_line = [(5, 0, 0)]  # Clear existing order lines
#                 order.order_line = [(0, 0, {
#                     'product_id': product.id,
#                     'name': product.display_name,
#                     'product_qty': 1,
#                     'product_uom': product.uom_id.id,
#                     'price_unit': product.standard_price,  # Use cost price
#                     'date_planned': fields.Datetime.now()
#                 }) for product in order.vendor_product_ids]