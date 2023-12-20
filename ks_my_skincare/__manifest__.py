{
    'name': 'KS - MySM',
    'summary': 'Ksolves Customization',
    'description': """ Ksolves customization
""",
    'author': 'Ksolves',
    'website': 'https://www.ksolves.com/',
    'depends': ['product', 'mysm_inventory', 'mysm_manufacturing'],
    'data': [
        'views/product_views.xml',
        'views/product_common_views.xml',
        'views/mrp_bom_views.xml',
        'views/stock_quant_views.xml',
        'wizard/generate_pif_report_wizard_views.xml',
        'report/product_pif_report.xml',
        'report/mo_pif_report.xml',
    ],
    'installable': True,
    'auto_install': True,
}
