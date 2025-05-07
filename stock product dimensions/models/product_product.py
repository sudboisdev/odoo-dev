from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    length = fields.Float(related="product_tmpl_id.length", store=True)
    width = fields.Float(related="product_tmpl_id.width", store=True)
    thickness = fields.Float(related="product_tmpl_id.thickness", store=True)

    stock_m2 = fields.Float(string="Stock (m²)", compute="_compute_stock_m2_m3", store=True)
    stock_m3 = fields.Float(string="Stock (m³)", compute="_compute_stock_m2_m3", store=True)

    price_per_m2 = fields.Monetary(
        related='product_tmpl_id.price_per_m2', store=True, readonly=True, currency_field='currency_id')
    price_per_m3 = fields.Monetary(
        related='product_tmpl_id.price_per_m3', store=True, readonly=True, currency_field='currency_id')

    @api.depends('qty_available', 'length', 'width', 'thickness')
    def _compute_stock_m2_m3(self):
        for product in self:
            if product.length and product.width:
                l = product.length / 1000
                w = product.width / 1000
                h = product.thickness / 1000 if product.thickness else 0
                product.stock_m2 = product.qty_available * l * w
                product.stock_m3 = product.qty_available * l * w * h if h else 0
            else:
                product.stock_m2 = 0
                product.stock_m3 = 0
