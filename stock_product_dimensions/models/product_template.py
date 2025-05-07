from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float("Longueur (mm)")
    width = fields.Float("Largeur (mm)")
    thickness = fields.Float("Épaisseur (mm)")

    
    area_m2 = fields.Float(string='Surface (m²)', compute='_compute_area_volume', store=True, digits=(12, 4))
    volume_m3 = fields.Float(string='Volume (m³)', compute='_compute_area_volume', store=True, digits=(12, 6))

    price_per_m2 = fields.Monetary(string="Prix au m²", compute="_compute_price_per_m2", store=True, currency_field='currency_id')
    price_per_m3 = fields.Monetary(string="Prix au m³", compute="_compute_price_per_m3", store=True, currency_field='currency_id')

    @api.depends('list_price', 'area_m2')
    def _compute_price_per_m2(self):
        for product in self:
            if product.area_m2 > 0:
                product.price_per_m2 = product.list_price / product.area_m2
            else:
                product.price_per_m2 = 0.0

    @api.depends('list_price', 'volume_m3')
    def _compute_price_per_m3(self):
        for product in self:
            if product.volume_m3 > 0:
                product.price_per_m3 = product.list_price / product.volume_m3
            else:
                product.price_per_m3 = 0.0
  
    @api.depends('length', 'width', 'thickness')
    def _compute_area_volume(self):
        for product in self:
            length_m = product.length / 1000
            width_m = product.width / 1000
            thickness_m = product.thickness / 1000

            product.area_m2 = length_m * width_m if product.length and product.width else 0.0
            product.volume_m3 = length_m * width_m * thickness_m if product.length and product.width and product.thickness else 0.0

