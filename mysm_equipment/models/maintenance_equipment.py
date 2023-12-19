# coding: utf-8
from odoo import api, fields, models, _
try:
    import qrcode
except ImportError:
    qrcode = None
import base64
from io import BytesIO
from odoo import http


class MaintenanceEquipment(models.Model):
    """ Inherit Maintenance Equipment"""
    _name = 'maintenance.equipment'
    _inherit = ['maintenance.equipment', 'avatar.mixin']

    sku_name = fields.Char('SKU', tracking=True, copy=False)
    criticality_id = fields.Many2one(
        'maintenance.criticality', string='Criticality', 
        change_default=True, index=True, tracking=1,)
    image = fields.Binary('Image', help="File image", attachment=True)
    image_package = fields.Binary('Image Package', help="Image Package", attachment=True)
    qr_code = fields.Binary("QR Code", store=True)
    note = fields.Text("Note")

    # _sql_constraints = [
    #     ('sku_name_uniq', 'unique(sku_name)', "A SKU can only be assigned to one equipment !"),
    # ]

    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_current_page = '%s/web#id=%s&model=maintenance.equipment&view_type=form' % (base_url, self.id)
        qr.add_data(url_current_page)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image
