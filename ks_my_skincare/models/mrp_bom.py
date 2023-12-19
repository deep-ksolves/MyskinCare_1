from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    components_ids = fields.One2many('mysm.component.composition', 'mrp_bom_id', string='Ingredients')

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
        ingredients = self.env['product.template'].search([('id', '=', self.product_tmpl_id.id)]).component_ids
        if ingredients:
            self.components_ids = [(5, 0, 0)]
            self.components_ids = [(6 ,0 ,ingredients.ids)]
        for value in allergen_dict.values():
            allergen_list.append((0, 0, value))
        self.allergen_composition_ids = allergen_list
