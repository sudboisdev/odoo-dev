from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    area_m2 = fields.Float(string="Surface unitaire (m²)", compute="_compute_unit_dimensions", store=True)
    volume_m3 = fields.Float(string="Volume unitaire (m³)", compute="_compute_unit_dimensions", store=True)

    area_total_m2 = fields.Float(string="Surface totale (m²)")
    volume_total_m3 = fields.Float(string="Volume totale (m³)")


    product_uom_qty_int = fields.Integer(
        string="Quantité (entière)",
        compute="_get_qty_int",
        inverse="_set_qty_int"
    )

    stock_alert_message = fields.Html(string="Alerte Stock", compute="_compute_stock_alert")

    @api.depends('product_id')
    def _compute_unit_dimensions(self):
        for line in self:
            tmpl = line.product_id.product_tmpl_id
            line.area_m2 = tmpl.area_m2 or 0.0
            line.volume_m3 = tmpl.volume_m3 or 0.0

    @api.onchange('area_total_m2')
    def _onchange_area_total_m2(self):
        for line in self:
            if line.area_m2:
                qty = line.area_total_m2 / line.area_m2
                line.product_uom_qty = int(round(qty))
                line.volume_total_m3 = line.product_uom_qty * line.volume_m3

    @api.onchange('volume_total_m3')
    def _onchange_volume_total_m3(self):
        for line in self:
            if line.volume_m3:
                qty = line.volume_total_m3 / line.volume_m3
                line.product_uom_qty = int(round(qty))
                line.area_total_m2 = line.product_uom_qty * line.area_m2

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        for line in self:
            line.area_total_m2 = line.product_uom_qty * line.area_m2
            line.volume_total_m3 = line.product_uom_qty * line.volume_m3

    @api.depends('product_uom_qty')
    def _get_qty_int(self):
        for line in self:
            line.product_uom_qty_int = int(round(line.product_uom_qty))

    def _set_qty_int(self):
        for line in self:
            line.product_uom_qty = line.product_uom_qty_int
