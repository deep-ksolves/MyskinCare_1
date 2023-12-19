from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    document_count = fields.Integer('Document Count', compute='_compute_document_count')

    def _compute_document_count(self):
        read_group_var = self.env['documents.document'].read_group(
            [('product_id', 'in', self.ids)],
            fields=['product_id'],
            groupby=['product_id'])

        document_count_dict = dict((d['product_id'][0], d['product_id_count']) for d in read_group_var)
        for record in self:
            record.document_count = document_count_dict.get(record.id, 0)

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'domain': [('product_id', '=', self.id)],
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                'default_product_id': self.id,
                'searchpanel_default_folder_id': False
            },
        }
