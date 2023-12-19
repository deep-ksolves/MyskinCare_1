from odoo import models, fields, _


class Documents(models.Model):
    _inherit = "documents.document"

    product_id = fields.Many2one('product.template', string="Product", tracking=True)
