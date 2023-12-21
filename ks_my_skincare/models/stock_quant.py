from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.quant"

    supplier_id = fields.Many2one('res.partner', 'Supplier', compute="_compute_supplier_id")

    def _compute_supplier_id(self):
        for record in self:
            stock_owner = self.env['product.product'].search([('id', '=', record.product_id.id)]).stock_ownership

            if stock_owner and stock_owner == 'owned_by_mysm':
                purchase_orders = record.lot_id.purchase_order_ids.sorted(key=lambda r: r.create_date, reverse=True)
                record.supplier_id = purchase_orders[0].partner_id.id if purchase_orders else False
            else:
                record.supplier_id = record.owner_id.id if record.owner_id else False

    def _get_inventory_fields_create(self):
        allowed_fields = super(StockMove, self)._get_inventory_fields_create()
        allowed_fields += ['supplier_id']
        return allowed_fields
