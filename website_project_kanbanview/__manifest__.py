# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': "Website Project Kanban View",
    'version': '15.0.0.1',
    'author': 'Geminate Consultancy Services',
    'desciption': """Geminate comes with a feature to introduce kanbanview for project and their related task on website. it will show the progress of each task based on their stage and due date.""",
    'summary':"""Website Project Kanban View""",
    'license': 'Other proprietary',
    'website': 'www.geminatecs.com',
    'category': 'Website',
    'depends': ['base','project','website'],
    'data': [
             'views/project_portal_templates.xml',
             'views/res_setting.xml'
            ],

    'assets': {
        'web.assets_frontend': [
            'website_project_kanbanview/static/src/js/geminate_kanban_view.js',
            'website_project_kanbanview/static/src/css/style.css',
        ],
    },

    'installable': True,
    'images': ['static/description/project-kanbanview.jpg'],
    'auto_install': False,
    'application': False,
    "price": 49.99,
    "currency": "USD"
}
