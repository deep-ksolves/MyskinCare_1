from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    same_category = fields.Boolean(string='Same Category', default=True)
    allergen_composition_ids = fields.One2many('mysm.allergen.composition.bom', 'mrp_bom_id', string='Allergen')
    total_component_percentage = fields.Float('Total Percentage', compute="_compute_total_percentage")

    @api.onchange('bom_line_ids')
    def check_category(self):
        for record in self:
            same_category = True
            product_uom_category = record.product_uom_id.category_id
            for line_id in record.bom_line_ids:
                line_product_uom_category = line_id.product_uom_id.category_id
                if line_product_uom_category.id != product_uom_category.id:
                    same_category = False
                    break
            record.same_category = same_category

    def _compute_total_percentage(self):
        for rec in self:
            rec.total_component_percentage = sum([line.percentage for line in rec.bom_line_ids])

    def update_formulation_button(self):
        for rec in self:
            formulation_update = rec.get_nb_ingredients_formulation()
            product_tmpl_id = rec.product_tmpl_id
            product_tmpl_id.write({
                'total_ingredients' : formulation_update.get('total_in'),
                'total_co_ingredients' : formulation_update.get('total_co_in'),
                'total_natural_ingredients' : formulation_update.get('total_nat_in'),
                'total_synthetic_ingredients' : formulation_update.get('total_syn_in'),
                'total_co_percentage' : formulation_update.get('total_co_per'),
                'total_natural_percentage' : formulation_update.get('total_nat_per'),
                'total_synthetic_percentage' : formulation_update.get('total_syn_per'),
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': "Update Formulation Success.",
                    'type': 'success',
                    'sticky': False,
                }
            }
            

    def action_compute(self):
        product_uom = self.product_uom_id
        product_uom_category = product_uom.category_id
        allergen_dict = {}
        # delete before add allergen
        allergen_list = [(5, 0, 0)]
        for line in self.bom_line_ids:
            line_product_uom = line.product_uom_id
            # check same unit of measure (UOM) category
            if line_product_uom.category_id.id == product_uom_category.id:
                # change QTY reference UOM to bom line UOM
                line_quantity = self.product_qty * line.percentage / 100
                line.product_qty = product_uom._compute_quantity(line_quantity, line_product_uom)
                # change RM Source
                line_product_rm_source_id = line.product_id.raw_material_source_id
                line.rm_source_id = line_product_rm_source_id if line_product_rm_source_id else False
                # search all allergen have the product_id in uom_line from allergen_composition
                allergens = self.env['mysm.allergen.composition'].search([('product_id', '=', line.product_id.id)])
                for allergen in allergens:
                    allergen_product_id = allergen.product_id.id
                    allergen_id = allergen.allergen_id.id
                    percent_formulation = (allergen.percentage * line.percentage) / 100
                    if allergen_id not in allergen_dict:
                        allergen_dict[allergen_id] = {
                            'allergen_id': allergen_id,
                            'product_ids': [(6, 0, [allergen_product_id])],
                            'mrp_bom_id': self.id,
                            'percent_formulation': percent_formulation
                        }
                    else:
                        product_ids = allergen_dict[allergen_id]['product_ids'][0][2]
                        product_ids.append(allergen_product_id)
                        allergen_dict[allergen_id].update({
                            'product_ids': [(6, 0, product_ids)],
                            'percent_formulation': allergen_dict[allergen_id]['percent_formulation'] + percent_formulation
                        })
            else:
                continue
        for value in allergen_dict.values():
            allergen_list.append((0, 0, value))
        self.allergen_composition_ids = allergen_list

    def compute_button(self):
        self.ensure_one()
        self.action_compute()
