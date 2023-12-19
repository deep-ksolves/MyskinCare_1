# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, models, tools


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    project_category_id = fields.Many2one("project.category",
                                          string="Project Category")

#    def _select(self):
#        select = super(ReportProjectTaskUser, self)._select()
#        select += """,p.project_category_id"""
#        return select

#    def _from(self):
#        from_str =\
#            """project_task t join project_project p on (t.project_id=p.id)"""
#        return from_str

#    def _group_by(self):
#        group_by_str = """
#                GROUP BY
#                    t.id,
#                    t.create_date,
#                    t.write_date,
#                    t.date_start,
#                    t.date_end,
#                    t.date_deadline,
#                    t.date_last_stage_update,
#                    t.user_id,
#                    t.project_id,
#                    t.priority,
#                    t.name,
#                    t.company_id,
#                    t.partner_id,
#                    t.stage_id,
#                    p.project_category_id
#        """
#        return group_by_str

#    def init(self):
#        tools.drop_view_if_exists(self._cr, self._table)
#        self.env.cr.execute("""CREATE VIEW %s as (
#                    %s
#                    FROM ( %s )  WHERE t.active = 'true'
#                    %s
#                    )""" % (
#        self._table, self._select(), self._from(), self._group_by()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
