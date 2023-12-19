from odoo import models, fields, api, _


class MRPBom(models.Model):
    _inherit = "mrp.bom"

    def open_generate_pif_report_wizard(self, report_type=False):
        if not type:
            return False
        components = self.mapped('bom_line_ids').mapped('product_id').filtered(lambda x: x.product_group == report_type)
        action = self.env["ir.actions.actions"]._for_xml_id("mysm_inventory.mysm_generate_pif_report_wizard_action")
        name = 'Raw Material' if report_type == 'raw_material' else 'Packaging'
        action.update({
            'context': {'default_domain_product_ids': components.ids, 'default_report_type': report_type},
            'name': '%s %s' % (action['name'], name),
            'target': 'new'
        })
        return action

    def generate_report_pif_for_formulation(self):
        report = self.env.ref('mysm_inventory.action_report_pif_for_formulation')
        return report.report_action(self, config=False)

    def generate_ingredient_list(self):
        self.ensure_one()
        ingredient_list = []
        for bom_line in self.bom_line_ids.sorted('percentage', reverse=True):
            product = bom_line.product_id
            if product.product_group == 'raw_material':
                ingredient = product.name
                if bom_line.rm_source_id and 'Organic' in bom_line.rm_source_id.name:
                    ingredient = '*' + ingredient
                ingredient_list.append(ingredient)
        ingredient_string = ', '.join(ingredient_list)
        return ingredient_string

    def calculate_nb_ingredients(self):
        total_in, total_co_in, total_qty = 0, 0, 0
        for rec in self:
            for bom_line in rec.bom_line_ids.sorted('percentage', reverse=True):
                product = bom_line.product_id
                if bom_line.rm_source_id and product.product_group == 'raw_material':
                    total_in += 1
                    if 'Organic' in bom_line.rm_source_id.name:
                        total_co_in += 1
                        total_qty += bom_line.product_qty
        return total_in, total_co_in, total_qty

    def get_nb_ingredients_formulation(self):
        self.ensure_one()
        total_in, total_co_in, total_nat_in, total_syn_in = 0, 0, 0, 0
        total_co_per, total_nat_per, total_syn_per = 0, 0, 0
        for bom_line in self.bom_line_ids:
            total_in += 1
            if bom_line.rm_source_id.name == 'Natural':
                total_nat_in += 1
                total_nat_per += bom_line.percentage
            elif bom_line.rm_source_id.name == 'Synthetic':
                total_syn_in += 1
                total_syn_per += bom_line.percentage
            elif bom_line.rm_source_id and 'Organic' in bom_line.rm_source_id.name:
                total_co_in += 1
                total_co_per += bom_line.percentage
        return {
            'total_in': total_in, 'total_co_in': total_co_in, 'total_nat_in': total_nat_in,
            'total_syn_in': total_syn_in, 'total_co_per': total_co_per,
            'total_nat_per': total_nat_per, 'total_syn_per': total_syn_per
        }
