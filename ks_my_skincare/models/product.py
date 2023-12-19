from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_components = fields.Boolean(string="Components", default=False)
    component_ids = fields.One2many(comodel_name='mysm.component.composition', inverse_name='product_id')

    @api.onchange('has_components')
    def delete_all_records(self):
        for product in self:
            if not product.has_components:
                records_to_delete = self.env['mysm.component.composition'].search([('product_id.name', '=', self.name)])
                records_to_delete.unlink()

    def action_component(self):
        action = {
            'name': 'Product Components ',
            'type': 'ir.actions.act_window',
            'res_model': 'mysm.component.composition',
            'view_mode': 'tree',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id}
        }
        return action

    def component_button(self):
        self.ensure_one()
        action = self.action_component()
        return action


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_component(self):
        action = {
            'name': 'Product Components ',
            'type': 'ir.actions.act_window',
            'res_model': 'mysm.component.composition',
            'view_mode': 'tree',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id}
        }
        return action

    def component_button(self):
        self.ensure_one()
        action = self.action_component()
        return action


class Saleorder(models.Model):
    _inherit = "sale.order"

    origin = fields.Char(string='Source Document', help="Reference of the document that generated this sales order request.", tracking=True)
