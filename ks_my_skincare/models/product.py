from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_allergens = fields.Boolean(string="Allergens", compute="check_allergens")
    pet_test_required = fields.Boolean(string="Pet Test Requested")
    stability_test_required = fields.Boolean(string="Stability Test Requested")
    product_benefits = fields.Text(string="Label claims:")
    clinical_tests_passed = fields.Text(string="Clinical Tests Passed")
    label_fill_volume_weight = fields.Float(string="Label fill Volume /Weight")
    min_fill_weight = fields.Float(string="Min. Fill Weight (g)")
    max_fill_weight = fields.Float(string="Max. Fill Weight (g)")
    converted_fill_weight = fields.Float(string="Converted fill Weight (g)")
    image_package2 = fields.Binary(
        'Image Package 2', help="Image Package 2", attachment=True)
    label_position_image = fields.Binary(
        'Label position image', help="Label Position Image", attachment=True)
    batch_number_image = fields.Binary(
        'Batch number image', help="Batch Number Image", attachment=True)
    detailed_image = fields.Binary(
        'Some other detailed images', help="Label Position Image", attachment=True)

    def check_allergens(self):
        template_id = self.product_variant_id.ids
        allergen = self.env['mysm.allergen.composition'].search_count([('product_id', 'in', template_id)])
        self.has_allergens = True if allergen else False


class ProductProduct(models.Model):
    _inherit = "product.product"

    allergen_ids = fields.One2many("mysm.allergen.composition", "product_id")

    @property
    def sorted_allergen_ids(self):
        return sorted(self.allergen_ids, key=lambda a: a.percentage, reverse=True)

    def generate_list_of_allergen(self):
        self.ensure_one()
        allergen_list = []

        if self.product_group == 'raw_material':
            allergens = self.env['mysm.allergen.composition'].search([('product_id', '=', self.id)]).mapped(
                'allergen_id').mapped('name')
            for allergen in allergens:
                ingredient = allergen if not allergen_list else allergen
                allergen_list.append(ingredient)

        allergen_string = ', '.join(allergen_list)
        return allergen_string

    def get_batches_of_ingredients(self):
        self.ensure_one()
        batches = self.env['stock.quant'].search(
            [('product_id', '=', self.id), ('location_id.usage', '=', 'internal')])

        result = []

        for batch in batches:
            supplier = batch.supplier_id.name
            batch_number = batch.lot_id.name
            date_of_arriving = batch.inventory_date
            expiration_date = batch.lot_id.expiration_date.date() if batch.lot_id.expiration_date else False
            available_stock = batch.available_quantity
            on_hand = batch.quantity
            wh_location = batch.location_id.name

            result.append({
                'supplier': supplier,
                'batch_number': batch_number,
                'date_of_arriving': date_of_arriving,
                'expiration_date': expiration_date,
                'available_stock': available_stock,
                'on_hand': on_hand,
                'wh_location': wh_location
            })

        return result
