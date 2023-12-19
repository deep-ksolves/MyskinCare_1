from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MySMComponentComposition(models.Model):
    _name = 'mysm.component.composition'
    _description = 'MySM Component Compositon'

    component_id = fields.Many2one(comodel_name="mysm.component", string='Component')
    percentage = fields.Float(string='% in Product')
    product_id = fields.Many2one(comodel_name="product.template", string="Product")
    mrp_bom_id = fields.Many2one(comodel_name="mrp.bom")
