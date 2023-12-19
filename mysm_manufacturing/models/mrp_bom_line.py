from odoo import fields, api, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    _order = "percentage desc, sequence, id"

    percentage = fields.Float(string='Percentage %')
    rm_source_id = fields.Many2one('mysm.attribute', string='RM Source', related='product_id.product_tmpl_id.raw_material_source_id')
