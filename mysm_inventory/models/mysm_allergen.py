from odoo import fields, models, api
from odoo.exceptions import ValidationError

class MySMAllergen(models.Model):
    _name = 'mysm.allergen'
    _description = 'MySM Allergen'

    name = fields.Char(string='Allergen', required=True)

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            unique_count = record.search_count([
                ('name', 'ilike', record.name),
                ('id', '!=', record.id)])
            if unique_count:
                raise ValidationError('Allergen must be unique')