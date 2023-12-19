{
    "name": "Non-Production Mode",
    "version": "1.0",
    "depends": ["base", "web_environment_ribbon"],
    "author": "Mplus Software, Odoo Community Association (OCA)",
    "category": "base",
    "description": """
    Base Module for Non-Production Mode
    """,
    "data": ["views/res_config_settings_views.xml"],
    "installable": True,
    "post_init_hook": "_nonproductionmode_post_init",
    "license": "LGPL-3",
}
