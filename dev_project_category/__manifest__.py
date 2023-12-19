# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Project Category',
    'version': '1.0',
    'sequence': 1,
    'category': 'Project',
    'description':
        """
This Module add below functionality into odoo

        1.Separate menu for creating category of Project\n
        3.Assign Category to the Project\n
        4.You can group by Projects by its Category\n
        5.Select project everywhere by its category\n
        
Project category 
Odoo project category 
Manage project category 
Odoo manage project category 
By Using this odoo application you can configure category of project and assign category to the project.
Separate menu for creating category of Project
Odoo Separate menu for creating category of Project
Assign Category to the Project
Odoo Assign Category to the Project
You can group by Project by its Category
Odoo You can group by Project by its Category
Select Project everywhere by its Category
Odoo Select Project everywhere by its Category
Category of project is shown in Project Dashboard
Odoo Category of project is shown in Project Dashboard
Configure project category 
Odoo configure project category 
Assign project category to project 
Odoo assign project category to project 

    """,
    'summary': 'odoo app will add Category into Project screen, Project Category,category of Project,Assign Category to the Project,group by Project Category',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_category_views.xml',
        'views/project_views.xml',
        'views/project_report_views.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':10.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
