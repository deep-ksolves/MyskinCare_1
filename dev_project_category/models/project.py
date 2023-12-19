# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api
from odoo.osv import expression


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if operator in ('ilike', 'like', '=', '=like', '=ilike'):
            domain = expression.AND(
                [args or [], ['|', ('name', operator, name),
                              ('project_category_id.code',
                               operator, name)]])
            return self.search(domain, limit=limit).name_get()
        return super(Project, self).name_search(
            name, args, operator, limit)

    project_category_id = fields.Many2one("project.category", string="Category")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
