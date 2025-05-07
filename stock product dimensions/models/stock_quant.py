from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    stock_m2 = fields.Float("Stock (m²)", compute="_compute_stock_area_volume", store=True)
    stock_m3 = fields.Float("Stock (m³)", compute="_compute_stock_area_volume", store=True)

    @api.depends('quantity', 'product_id.length', 'product_id.width', 'product_id.thickness')
    def _compute_stock_area_volume(self):
        for quant in self:
            if quant.product_id.length and quant.product_id.width:
                l = quant.product_id.length / 1000
                w = quant.product_id.width / 1000
                h = quant.product_id.thickness / 1000 if quant.product_id.thickness else 0
                quant.stock_m2 = quant.quantity * l * w
                quant.stock_m3 = quant.quantity * l * w * h if h else 0
            else:
                quant.stock_m2 = 0
                quant.stock_m3 = 0
