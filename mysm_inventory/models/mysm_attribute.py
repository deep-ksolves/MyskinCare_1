from odoo import models, fields, api


class MysmAttribute(models.Model):
    _name = "mysm.attribute"
    _description = "MySM Attribute"

    name = fields.Char(string="Name", required=True)
    field_name = fields.Char(string="Model Name")
