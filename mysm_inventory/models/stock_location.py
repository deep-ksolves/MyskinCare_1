try:
    import qrcode
except ImportError:
    qrcode = None
import base64
from io import BytesIO
from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    lot_ribbon_id = fields.Many2one("product.ribbon", "Lot Ribbon")

    def generate_qr_code(self):
        self.ensure_one()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_current_page = '%s/web#id=%s&model=stock.location&view_type=form' % (base_url, self.id)
        qr.add_data(url_current_page)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image