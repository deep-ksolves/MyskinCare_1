{
    'name': 'KS - MySM',
    'summary': 'Access components from the Inventory/products',
    'description': """
Easily access any product components from your product profile.
""",
    'author': 'Ksolves',
    'version': '15.0.0.1',
    'website': 'https://www.ksolves.com/',
    'depends': ['product', 'mysm_inventory', 'mysm_manufacturing', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/mysm_component_views.xml',
        'views/mysm_component_composition.xml',
        'views/mrp_bom_views.xml',
        'report/mo_pif_report.xml',
    ],
    'installable': True,
    'auto_install': True,
}
