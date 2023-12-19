from odoo import _, api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mysm_number = fields.Char(string="MySM Number",related='product_id.product_tmpl_id.default_code')
    vendor_part_no = fields.Char(string='Vendor Part No',related='product_id.product_tmpl_id.name')
    mysm_description = fields.Char(string='Description')

    @api.onchange('product_id')
    def onchange_mysm_description(self):
        for rec in self:
            rec.mysm_description = rec.product_id.product_tmpl_id.display_name