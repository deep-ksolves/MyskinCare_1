from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    payment_gateway = fields.Char(string='Payment Gateway')
    bank_account_id = fields.Many2one('res.partner.bank', string='Bank Account')
    bsb = fields.Char(string='BSB')