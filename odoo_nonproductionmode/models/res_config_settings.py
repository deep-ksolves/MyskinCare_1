from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_non_production_mode = fields.Boolean(default=False, string="Activate non production mode")
    user_password = fields.Char(help="this password will be used during testing mode", default="demodemo")
    header_color = fields.Char(default="#eba834")
    custom_sql = fields.Text()

    def get_db_name(self):
        return self.env.cr.dbname

    db_name = fields.Char(compute="_compute_getdbname", default=get_db_name)

    def _compute_getdbname(self):
        for rec in self:
            rec.db_name = self.get_db_name()

    def set_values(self):
        self.env["ir.config_parameter"].set_param("is_non_production_mode", str(self.is_non_production_mode))
        self.env["ir.config_parameter"].set_param("user_password", str(self.user_password))
        self.env["ir.config_parameter"].set_param("header_color", str(self.header_color))
        self.env["ir.config_parameter"].set_param("custom_sql", self.custom_sql)

        super(ResConfigSettings, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            is_non_production_mode=self.env["ir.config_parameter"].get_param("is_non_production_mode") == "True",
            user_password=self.env["ir.config_parameter"].get_param("user_password") or "",
            header_color=self.env["ir.config_parameter"].get_param("header_color") or "#eba834",
            custom_sql=self.env["ir.config_parameter"].get_param("custom_sql") or "",
        )
        return res

    def save_wizard_form(self):
        self.set_values()

    def activate_non_prod_mode(self):
        self.env["ir.config_parameter"].set_param("is_non_production_mode", str(True))
        self.env["ir.config_parameter"].set_param("ribbon.name", "NON-PROD<br/>({db_name})")
        self.change_email_res_partner()
        self.change_user_password()
        self.deactivate_incoming_email()
        self.run_custom_query()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def confirm_activate_non_prod_mode(self):
        if "prod" in self.get_db_name():
            raise ValidationError("The name of the database used contains the word ‘PROD’, please check again.")
        self.set_values()

        self.write({"header_color": self.header_color})
        view = self.env.ref("odoo_nonproductionmode.confirm_enter_to_none_production_form")
        return {
            "name": _("Confirm activation of the Non-Production mode"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "res.config.settings",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            # 'res_id': wiz.id,
            "context": self.env.context,
        }

    def change_email_res_partner(self):
        for partner in self.env["res.partner"].search([]):
            if partner.email:
                email_prod = partner.email
                email = partner.email.split("@")[0] + "@yopmail.com"
                partner.write({"email": email, "email_prod": email_prod})

    def change_user_password(self):
        for rec in self.env["res.users"].search([("id", "!=", self.env.user.id)]):
            rec.write({"password": self.user_password})

    def deactivate_incoming_email(self):
        """Deactivate fetchmail server if installed"""
        try:
            for rec in self.env["fetchmail.server"].search([]):
                rec.write({"active": False})
        except KeyError:
            pass

    def run_custom_query(self):
        if self.custom_sql:
            self.env.cr.execute(self.custom_sql)

    def deactivate_non_prod_mode(self):
        try:
            for rec in self.env["fetchmail.server"].search([("active", "=", False)]):
                rec.write({"active": True})
        except KeyError:
            pass

        for partner in self.env["res.partner"].search([]):
            partner.write({"email": partner.email_prod, "email_prod": None})

        self.env["ir.config_parameter"].set_param("is_non_production_mode", str(False))
        self.env["ir.config_parameter"].set_param("ribbon.name", str(False))

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def confirm_deactivate_non_prod_mode(self):
        if "prod" in self.get_db_name():
            raise ValidationError("The name of the database used contains the word ‘PROD’, please check again.")
        view = self.env.ref("odoo_nonproductionmode.confirm_enter_to_production_form")
        return {
            "name": _("Confirm Deactivation of the Non-Production mode"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "res.config.settings",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            # 'res_id': wiz.id,
            "context": self.env.context,
        }
