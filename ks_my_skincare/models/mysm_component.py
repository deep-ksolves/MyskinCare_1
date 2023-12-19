from odoo import models, fields, api


class MySMComponent(models.Model):
    _name = 'mysm.component'
    _description = 'MySM Components'

    name = fields.Char(string='Name', required=True)
    inci_name = fields.Char(string="INCI Name")
    cas_number = fields.Char(string="CAS Number")

