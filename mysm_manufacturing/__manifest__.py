{
    'name': 'MySM - Manufacturing',
    'version': '15.0.0.1.0',
    'author': 'Port Cities',
    'website': 'https://www.portcities.net',
    'summary': "Inventory Customization",
    'description':
    """
    - Inventory Customization
    """,
    'depends': [
        'product',
        'purchase',
        'stock',
        'uom',
        'mysm_inventory'
    ],
    'data': [
        'views/mrp_bom_view.xml'
    ],
    'sequence': 1,
    'active': True,
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
