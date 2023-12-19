# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'MySM - Equipment',
    'version': '15.0.0.1.0',
    'author': 'Port Cities',
    'website': 'https://www.portcities.net',
    'summary': """Equipment Customization""",
    'description':
                """
                - Equipment Detail Improvement \n
                by Kamal\n
                - Migrating to v15\n
                by WS
                """,
    'depends': [
        'hr',
        'mrp_maintenance'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_criticality_view.xml',
        'views/maintenance_equipment_view.xml',
        'views/mysm_contact_views.xml',
        'report/equipment_label_report.xml',
        'report/equipment_report.xml',
    ],
    'sequence1': 1,
    'active': True,
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'mysm_equipment/static/src/js/image_field.js',
        ],
    }
}
