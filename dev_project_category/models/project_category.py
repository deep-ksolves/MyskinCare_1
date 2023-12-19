# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, _


class ProjectCategory(models.Model):
    _name = "project.category"
    _description = "Category of Project"

    name = fields.Char(string="Category")
    code = fields.Char(string="Code")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: