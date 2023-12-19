from odoo import http, _
from odoo.http import request
from odoo.addons.stock_barcode.controllers.main import StockBarcodeController


class StockBarcodeController(StockBarcodeController):

    def get_action_equipment(self, equipment_id):
        view_id = request.env.ref('maintenance.hr_equipment_view_form').id
        return {
            'action': {
                'name': _('Open Equipment form'),
                'res_model': 'maintenance.equipment',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'views': [(view_id, 'form')],
                'type': 'ir.actions.act_window',
                'res_id': equipment_id,
            }
        }

    def get_id_form_url(self, barcode):
        barcode_url = barcode
        split_url_by_id = barcode_url.split('id=')
        return split_url_by_id[-1][0]

    def try_open_equipment(self, barcode):
        equipment_id = self.get_id_form_url(barcode)
        corresponding_equipment = request.env['maintenance.equipment'].search([
            ('id', '=', equipment_id)], limit=1)
        if corresponding_equipment:
            return self.get_action_equipment(corresponding_equipment.id)
        return False

    @http.route()
    def main_menu(self, barcode, **kw):
        ret_open_mrp = self.try_open_equipment(barcode)
        if ret_open_mrp:
            return ret_open_mrp
        return super(StockBarcodeController, self).main_menu(barcode, **kw)
