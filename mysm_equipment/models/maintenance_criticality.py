# coding: utf-8
from odoo import api, fields, models, _

class MaintenanceCriticality(models.Model):
    """ New model Maintenance Criticality"""
    _name = 'maintenance.criticality'
    _description = 'Maintenance Criticality'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(string='Sequence', default=10)
