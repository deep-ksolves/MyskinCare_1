try:
    import qrcode
except ImportError:
    qrcode = None
import base64
from io import BytesIO

from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    lot_ribbon_id = fields.Many2one(
        "product.ribbon", "Lot Ribbon", compute="_compute_lot_ribbon")
    ribbon_html = fields.Html("Ribbon", compute="_compute_lot_ribbon")

    def generate_qr_code(self, model=False):
        self.ensure_one()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_model_name = model if model else self._name
        url_current_page = '%s/web#id=%s&model=%s&view_type=form' % (base_url, self.id, url_model_name)
        qr.add_data(url_current_page)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image

    def _get_stock_picking(self):
        lines = self.env['stock.move.line'].search([
            ('lot_id', '=', self.id),
            ('state', '=', 'done'),
        ])
        return lines.mapped('picking_id').sorted(key=lambda l: l['scheduled_date'])

    def _get_last_partner_id_stock_picking(self):
        picking_id = self._get_stock_picking()
        last_partner_id = False
        if picking_id:
            last_partner_id = picking_id[0].partner_id or False
        return last_partner_id

    def _compute_lot_ribbon(self):
        for rec in self:
            quants = self.env['stock.quant'].sudo().search(
                [('lot_id', '=', rec.id), ('location_id.usage', '=', 'internal')], order="id desc")
            lot_ribbon_id = False
            html = ''
            if quants:
                lot_ribbon = quants[0].location_id.lot_ribbon_id
                lot_ribbon_id = lot_ribbon.id
                style = ''
                if lot_ribbon.text_color:
                    style += 'color: %s;' % lot_ribbon.text_color
                if lot_ribbon.bg_color:
                    style += 'background-color: %s;' % lot_ribbon.text_color
                html = '''
                    <span class="%s" style="%s">
                        %s
                    </span>
                ''' % (lot_ribbon.html_class, style, lot_ribbon.html)
            rec.lot_ribbon_id = lot_ribbon_id
            rec.ribbon_html = html

    @api.model
    def _get_next_serial(self, company, product):
        """ Inherit _get_next_serial function"""
        res = super()._get_next_serial(company, product)
        if not res:
            res = self.env['ir.sequence'] \
                    .next_by_code('product.template.%s.sequence' % product.product_group)
        return res
