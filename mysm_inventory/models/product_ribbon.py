from odoo import models, fields


class ProductRibbon(models.Model):
    _inherit = "product.ribbon"

    is_lot_ribbon = fields.Boolean("Lot Ribbon")
