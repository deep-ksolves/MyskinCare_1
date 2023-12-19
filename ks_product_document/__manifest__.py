{
    'name': 'Product Template',
    'category': 'Productivity/Documents',
    'summary': 'Access documents from the Inventory/products',
    'description': """
Easily access your documents from your product profile.
""",
    'author': 'Ksolves',
    'website': 'https://www.ksolves.com/',
    'depends': ['documents', 'product', 'mrp'],
    'data': [
        'views/documents_document.xml',
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            ('replace', 'documents/static/src/js/documents_controller_mixin.js',
             'ks_product_document/static/src/js/documents_controller_mixin.js'),
        ],
    },
    'installable': True,
    'auto_install': True,
}
