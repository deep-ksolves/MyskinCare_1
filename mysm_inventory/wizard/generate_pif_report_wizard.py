from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MysmAllergenComposition(models.TransientModel):
    _name = 'generate.pif.report.wizard'
    _description = 'Generate PIF Report Wizard'

    domain_product_ids = fields.Many2many(
        'product.product', 'domain_product_wizard_rel', string="Domain Products")
    product_ids = fields.Many2many(
        'product.product', 'product_wizard_rel', string="Products")

    def button_print(self):
        self.ensure_one()
        if self.product_ids:
            report = self.env.ref('mysm_inventory.action_report_pif')
            return report.report_action(self.product_ids, config=False)
        return True
