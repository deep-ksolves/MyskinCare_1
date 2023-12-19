from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    def get_components(self):
        component_list = []
        products = self.env['product.product'].search([('id', 'in', self.product_id.ids)])
        for product in products:
            template = self.env['product.template'].search([('id', '=', product.product_tmpl_id.id)])
            components = self.env['mysm.component.composition'].search([('product_id', '=', template.id)])
            for component in components:
                name = self.env['mysm.component'].search([('id', '=', component.component_id.id)]).name
                percentage = component.percentage
                component_dict = {'name': name,
                                  'percentage': percentage}
                component_list.append(component_dict)
        return component_list
