from odoo import _, api, fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    swift_code = fields.Char(string='Swift Code')
