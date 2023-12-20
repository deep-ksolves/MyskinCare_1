from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    has_allergen = fields.Boolean(compute="check_allergen")
    mo_ids = fields.One2many('mrp.production', 'bom_id', string="Manufacturing Order")

    def generate_report_pif_for_formulation(self, val):
        if val == 'External':
            report = self.env.ref('ks_my_skincare.action_report_pif_for_formulation_external')
        else:
            report = self.env.ref('ks_my_skincare.action_report_pif_for_formulation_internal')
        return report.report_action(self, config=False)

    def generate_allergen_list(self):
        self.ensure_one()
        allergen_set = set()

        for bom_line in self.bom_line_ids.sorted('percentage', reverse=True):
            product = bom_line.product_id
            if product.product_group == 'raw_material':
                allergens = self.env['mysm.allergen.composition'].search([('product_id', '=', product.id)]).mapped(
                    'allergen_id').mapped('name')
                for allergen in allergens:
                    ingredient = allergen if not allergen_set else allergen
                    allergen_set.add(ingredient)

        allergen_string = ', '.join(allergen_set)
        return allergen_string

    def check_allergen(self):
        count = 0
        for bom_line in self.bom_line_ids:
            if bom_line.product_id.product_tmpl_id.has_allergens:
                count += 1
        self.has_allergen = True if count > 0 else False
