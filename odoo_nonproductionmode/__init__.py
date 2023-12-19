from . import models

from odoo import api, SUPERUSER_ID

def _nonproductionmode_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.config_parameter"].set_param("ribbon.name", str(False))

