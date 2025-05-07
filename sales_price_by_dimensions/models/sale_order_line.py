from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True, readonly=True)

    price_unit = fields.Monetary(string="Prix unitaire", currency_field='currency_id')
    price_per_m2 = fields.Monetary(string="Prix au m²", currency_field='currency_id')
    price_per_m3 = fields.Monetary(string="Prix au m³", currency_field='currency_id')

    area_total_m2 = fields.Float(string="Surface totale (m²)")
    volume_total_m3 = fields.Float(string="Volume totale (m³)")

    unite_de_vente = fields.Selection([
        ('unit', 'Unitaire'),
        ('m2', 'm²'),
        ('m3', 'm³'),
    ], string="Unité de vente", default='unit')

    prix_udv = fields.Monetary(string="Prix UDV", currency_field='currency_id', readonly=True, store=False)

    @api.onchange('unite_de_vente', 'price_unit', 'price_per_m2', 'price_per_m3')
    def _onchange_prix_udv(self):
        if self.unite_de_vente == 'unit':
            self.prix_udv = self.price_unit
        elif self.unite_de_vente == 'm2':
            self.prix_udv = self.price_per_m2
        elif self.unite_de_vente == 'm3':
            self.prix_udv = self.price_per_m3

    @api.model
    def _get_product_dimensions(self):
        """Récupère les dimensions du produit en mètres."""
        length = self.product_id.length or 0.0
        width = self.product_id.width or 0.0
        thickness = self.product_id.thickness or 0.0
        area_m2 = (length / 1000) * (width / 1000)
        volume_m3 = area_m2 * (thickness / 1000)
        return area_m2, volume_m3

    @api.onchange('product_id')
    def _onchange_product_id_set_prices(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price or 0.0
            self.price_per_m2 = self.product_id.price_per_m2 or 0.0
            self.price_per_m3 = self.product_id.price_per_m3 or 0.0

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        area_m2, volume_m3 = self._get_product_dimensions()
        if area_m2:
            self.price_per_m2 = self.price_unit / area_m2
        else:
            self.price_per_m2 = 0.0
        if volume_m3:
            self.price_per_m3 = self.price_unit / volume_m3
        else:
            self.price_per_m3 = 0.0

    @api.onchange('price_per_m2')
    def _onchange_price_per_m2(self):
        area_m2, volume_m3 = self._get_product_dimensions()
        self.price_unit = self.price_per_m2 * area_m2 if area_m2 else 0.0
        if volume_m3:
            self.price_per_m3 = self.price_unit / volume_m3
        else:
            self.price_per_m3 = 0.0

    @api.onchange('price_per_m3')
    def _onchange_price_per_m3(self):
        area_m2, volume_m3 = self._get_product_dimensions()
        self.price_unit = self.price_per_m3 * volume_m3 if volume_m3 else 0.0
        if area_m2:
            self.price_per_m2 = self.price_unit / area_m2
        else:
            self.price_per_m2 = 0.0
