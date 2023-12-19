from odoo import models, fields, api, _


class MRPProduction(models.Model):
    _inherit = "mrp.production"

    def generate_report_mo_pif(self):
        report = self.env.ref('mysm_inventory.action_report_mo_pif')
        return report.report_action(self, config=False)
