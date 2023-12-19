from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MysmAllergenComposition(models.Model):
    _name = 'mysm.allergen.composition'
    _description = 'MySM Allergen Composition'

    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    allergen_id = fields.Many2one(
        'mysm.allergen', string='Allergen', required=True)
    percentage = fields.Float(string='% of Allergen')

    @api.constrains('product_id', 'allergen_id')
    def check_unique_product_allergen(self):
        for record in self:
            unique_count = record.search_count([
                ('product_id', '=', record.product_id.id),
                ('allergen_id', '=', record.allergen_id.id),
                ('id', '!=', record.id)
            ])
            if unique_count:
                product_name = record.product_id.name
                allergen_name = record.allergen_id.name
                raise ValidationError(
                    f'''The Allergen Composition combination you enter for {product_name} and {allergen_name} already exist.
Please check allergen list for {product_name} and update the value for {allergen_name} when necessary''')

class MysmAllergenCompositionBOM(models.Model):
    _name = 'mysm.allergen.composition.bom'
    _description = 'MySM Allergen Composition BoM'

    product_ids = fields.Many2many(
        'product.product', string='Products', required=True)
    mrp_bom_id = fields.Many2one('mrp.bom', string='MRP BoM')
    allergen_id = fields.Many2one(
        'mysm.allergen', string='Allergen', required=True)
    percent_formulation = fields.Float(string='FP Percentage %')
