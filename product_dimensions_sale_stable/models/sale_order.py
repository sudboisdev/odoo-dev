from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_area_m2 = fields.Float(string="Surface totale (m²)", compute="_compute_totals", store=True)
    total_volume_m3 = fields.Float(string="Volume totale (m³)", compute="_compute_totals", store=True)

    @api.depends('order_line.area_total_m2', 'order_line.volume_total_m3')
    def _compute_totals(self):
        for order in self:
            order.total_area_m2 = sum(line.area_total_m2 for line in order.order_line)
            order.total_volume_m3 = sum(line.volume_total_m3 for line in order.order_line)
