from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    def generate_lot_serial_number(self):
        for record in self:
            product = record.product_id
            if product.tracking == 'none':
                continue
            product_group = product.product_group
            lot_name = self.env["ir.sequence"].next_by_code("product.template.%s.sequence" % product_group)
            lot_id = self.env["stock.production.lot"].create({
                "product_id": product.id,
                "company_id": record.company_id.id,
                "name": lot_name,
            })
            create_qty = record.product_uom_qty - record.quantity_done
            if create_qty > 0:
                for line in record.move_line_ids:
                    if not line.lot_id and float_is_zero(line.qty_done, precision_rounding=0.1):
                        line.unlink()
                    else:
                        line.write({'product_uom_qty': line.qty_done})
                record.write({"move_line_ids": [(0, 0, {
                    "product_id": product.id,
                    "product_uom_id": record.product_uom.id,
                    "company_id": record.company_id.id,
                    "picking_id": record.picking_id.id,
                    "move_id": record.id,
                    "location_id": record.location_id.id,
                    "location_dest_id": record.location_dest_id.id,
                    "lot_name": lot_name,
                    "lot_id": lot_id.id,
                    "product_uom_qty": create_qty,
                    "qty_done": create_qty,
                })]})
