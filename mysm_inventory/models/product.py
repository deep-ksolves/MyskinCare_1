try:
    import qrcode
except ImportError:
    qrcode = None
import base64
import pytz
from io import BytesIO
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_code = fields.Char(string="MySM SKU Nr.")
    product_group = fields.Selection([
        ('raw_material', _('Raw Material')),
        ('raw_material_client', _('Raw Material Client')),
        ('finished_product', _('Finished Product')),
        ('packaging', _('Packaging')),
        ('packaging_client', _('Packaging Pack Client')),
        ('formulation', _('Formulation'))],
        required=True, default='raw_material', string="Product Group")
    form_id = fields.Many2one('mysm.attribute',
                              domain="[('field_name', '=', 'form.product')]", string="Form")
    raw_material_source_id = fields.Many2one('mysm.attribute',
                                             domain="[('field_name', '=', 'raw.material.source')]", string="Raw Material Source")
    inci_name = fields.Char(string="INCI Name")
    cas_number = fields.Char(string="CAS Number")
    product_description = fields.Text(string="Product Description")
    link_to_wiki = fields.Char(string="Link To Wikipedia")
    whs_handling = fields.Text(string="WHS Handling")
    whs_storage = fields.Text(string="WHS Storage")
    whs_fire = fields.Text(string="WHS Fire")
    whs_accident = fields.Text(string="WHS Accident")
    extraction_method_id = fields.Many2one('mysm.attribute',
                                           domain="[('field_name', '=', 'extract.method')]", string="Extraction Method")
    plant_part_id = fields.Many2one('mysm.attribute',
                                    domain="[('field_name', '=', 'plant.part')]", string="Plant Part")
    aromatherapy_note_id = fields.Many2one('mysm.attribute',
                                           domain="[('field_name', '=', 'aromatherapy.note')]", string="Aromatherapy Note")
    aromatic_category_id = fields.Many2one('mysm.attribute',
                                           domain="[('field_name', '=', 'aromatic.category')]", string="Aromatic Category")
    strength_of_aroma_id = fields.Many2one('mysm.attribute',
                                           domain="[('field_name', '=', 'strength.aroma')]", string="Strength of Aroma")
    brand_name_id = fields.Many2one("mysm.attribute",
                                    domain="[('field_name', '=', 'brand.name')]", string="Brand Name")
    type_of_packaging_id = fields.Many2one("mysm.attribute",
                                           domain="[('field_name', '=', 'type.packaging')]", string="Type of Packaging")
    type_of_material_id = fields.Many2one("mysm.attribute",
                                          domain="[('field_name', '=', 'type.material')]", string="Type of Material")
    type_of_dispenser_id = fields.Many2one("mysm.attribute",
                                           domain="[('field_name', '=', 'type.dispenser')]", string="Type of Dispenser")
    type_of_caps_id = fields.Many2one("mysm.attribute",
                                      domain="[('field_name', '=', 'type.caps')]", string="Type of Caps")
    shape_of_the_packaging_id = fields.Many2one("mysm.attribute",
                                                domain="[('field_name', '=', 'shape.packaging')]", string="Shape of the Packaging")
    basic_color_id = fields.Many2one("mysm.attribute",
                                     domain="[('field_name', '=', 'basic.color')]", string="Basic Colour")
    neck_size_id = fields.Many2one("mysm.attribute",
                                   domain="[('field_name', '=', 'neck.size')]", string="Neck Size")
    aromatic_description = fields.Text(string="Aromatic Description")
    emotional_profile = fields.Char(string="Emotional Profile")
    blends_well_with = fields.Text(string="Blends well with")
    country_of_origin_id = fields.Many2one(
        'res.country', string="Country of Origin")
    traditional_uses = fields.Text(string="Traditional Uses")
    key_benefits = fields.Text(string="Key benefits")

    product_benefits = fields.Text(string="Product benefits")
    aroma_description = fields.Text(string="Aroma Description")
    colour_description = fields.Text(string="Colour Description")

    dispensing_volume = fields.Char(string="Dispensing Volume")
    viscosity_range = fields.Char(string="Viscosity Range")
    ph_range = fields.Char(string="pH Range")

    product_dimensions = fields.Float(string="Product Dimensions")
    product_net_weight = fields.Float(string="Product Net Weight")
    product_gross_weight = fields.Float(string="Product Gross Weight")
    product_volume = fields.Float(string="Product Volume")
    ph_value = fields.Char(string="pH")
    specific_weight = fields.Char(string="Specific Weight")

    use_after_opening = fields.Integer(string="Use after Opening")

    packaging_status = fields.Selection([
        ('quarantine', 'Quarantine'),
        ('released', 'Released'),
        ('reject', 'Reject')], string="Packaging Status")
    stock_ownership = fields.Selection([
        ('owned_by_mysm', 'Owned by MySM'),
        ('client', 'Client')], string="Stock Ownership")
    formulation_type = fields.Selection([
        ('wash_off', 'Wash Off'),
        ('leave_on', 'Leave On')], string="Formulation Type")

    for_client_product_id = fields.Many2one(
        "product.product", string="For Client's Product")
    customer_id = fields.Many2one("res.partner", string="Customer")

    height = fields.Float(string="Height")
    height_uom_name = fields.Char(
        string='Height unit of measure label', default="mm")
    width = fields.Float(string="Width")
    width_uom_name = fields.Char(
        string='Width unit of measure label', default="mm")
    depth = fields.Float(string="Depth")
    depth_uom_name = fields.Char(
        string='Depth unit of measure label', default="mm")
    volume_for_logistic = fields.Float(
        string="Volume for Logistic", compute='_compute_volume_for_logistic', store=True)
    vol_logistic_uom_name = fields.Char(
        string='Volume Logistic unit of measure label', default="ml")
    count_composition = fields.Boolean(
        string='Count Composition', compute='_compute_count')

    image_package = fields.Binary(
        'Image Package', help="Image Package", attachment=True)

    def _compute_count(self):
        self.ensure_one()
        count_composition = self.env['mysm.allergen.composition'].search_count(
            [('product_id', '=', self.product_variant_id.id)])
        self.count_composition = True if count_composition else False

    viscosity = fields.Char(string="Viscosity")
    total_ingredients = fields.Integer(string="Total Ingredients")
    total_co_ingredients = fields.Integer(string="Total C.O. Ingredients")
    total_natural_ingredients = fields.Integer(
        string="Total Natural Ingredients")
    total_synthetic_ingredients = fields.Integer(
        string="Total Synthetic Ingredients")
    total_co_percentage = fields.Float(
        string="Total Content of C.O. Ingredients in %")
    total_natural_percentage = fields.Float(
        string="Total Content of Natural Ingredients in %")
    total_synthetic_percentage = fields.Float(
        string="Total Content of Synthetic Ingredients in %")

    @api.depends('width', 'height', 'depth')
    def _compute_volume_for_logistic(self):
        for rec in self:
            rec.volume_for_logistic = rec.height * rec.width * rec.depth / 1000

    appearance = fields.Char(string="Appearance")
    gmp_release_specs = fields.Text(string="Additional Releases Specifications")
    additional_characteristic_info = fields.Text(string="Additional Characteristic Information")
    additional_marketing_support_info = fields.Text(string="Additional Marketing Support Information")

    shelf_life = fields.Char(string="Shelf Life (month)")
    dimensions_additional_gmp_spec = fields.Text(string="Dimensions and Additional Release Specifications")
    additional_gmp_info_spec = fields.Text(string="Additional Release Information and Specifications")
    primary_product_id = fields.Many2one('product.template', string="Primary Product")
    other_product_id = fields.Many2one('product.template', string='Other Product')

    sale_internal_note = fields.Text(string="Sale Internal Note")
    inventory_internal_note = fields.Text(string="Inventory Internal Note")
    accounting_internal_note = fields.Text(string="Accounting Internal Note")
    rm_gmp_internal_note = fields.Text(string="Raw Material Specifications Internal Note")
    rm_characteristic_internal_note = fields.Text(string="Raw Material Characteristics Internal Note")
    packaging_specifications_internal_note = fields.Text(string="Package Specifications Internal Notes")
    packaging_characteristic_internal_note = fields.Text(string="Package Characteristic Internal Notes")
    formulation_specifications_internal_note = fields.Text(string="Formulation Specifications Internal Notes")
    formulation_characteristic_internal_note = fields.Text(string="Formulation Characteristic Internal Notes")
    fp_specifications_internal_note = fields.Text(string="Finished Product Specifications Internal Notes")
    fp_characteristic_internal_note = fields.Text(string="Finished Product Characteristic Internal Notes")

    list_of_components = fields.Text(string="List of Components")
    list_of_sevices = fields.Text(string="List of Services")
    pet_test_required = fields.Boolean(string="Pet Test Required")
    pet_test_passed_date = fields.Date(string="Pet Test Passed Date")
    stability_test_required = fields.Boolean(string="Stability Test Required")
    stability_test_passed_date = fields.Date(string="Stability Test Passed Date")
    clinical_test_required = fields.Boolean(string="Clinical Test Required")
    clinical_test_passed_date = fields.Date(string="Clinical Test Passed Date")

    @api.onchange('product_group')
    def onchange_product_group(self):
        for seller in self.seller_ids:
            seller.product_group = self.product_group

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `weight` field. By default, we considerer
        that weights are expressed in kilograms. Users can configure to express them in pounds
        by adding an ir.config_parameter record with "product.product_weight_in_lbs" as key
        and "1" as value.
        """
        product_weight_in_lbs_param = self.env['ir.config_parameter'].sudo(
        ).get_param('product.weight_in_lbs')
        if product_weight_in_lbs_param == '1':
            return self.env.ref('uom.product_uom_lb')
        else:
            return self.env.ref('uom.product_uom_gram')

    @api.model
    def _get_volume_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `volume` field. By default, we consider
        that volumes are expressed in cubic meters. Users can configure to express them in cubic feet
        by adding an ir.config_parameter record with "product.volume_in_cubic_feet" as key
        and "1" as value.
        """
        product_length_in_feet_param = self.env['ir.config_parameter'].sudo(
        ).get_param('product.volume_in_cubic_feet')
        if product_length_in_feet_param == '1':
            return self.env.ref('uom.product_uom_cubic_foot')
        else:
            return self.env.ref('mysm_inventory.product_uom_mililiter')

    def action_allergen(self):
        action = {
            'name': 'Allergen Composition ',
            'type': 'ir.actions.act_window',
            'res_model': 'mysm.allergen.composition',
            'view_mode': 'tree',
            'domain': [('product_id', '=', self.product_variant_id.id)],
            'context': {'default_product_id': self.product_variant_id.id}
        }
        return action

    def allergen_button(self):
        self.ensure_one()
        action = self.action_allergen()
        return action

    def generate_pif_report_for_product(self):
        for rec in self:
            if rec.product_group == 'formulation':
                raise UserError(_('''To print a PIF for Formulation. Please go to:\n
    Bill of Material > Select a BoM > Action > Generate PIF for Formulation.'''))
    #         elif rec.product_group == 'finished_product':
    #             raise UserError(_('''To print a PIF for Finished Product. Please go to:\n
    # Manufacturing Orders > Select a MO > Action > Generate PIF for Finished Product.'''))
            elif rec.product_group in ['raw_material_client', 'packaging_client']:
                raise UserError(_('Does not print PIF report for Raw Material Client and Packaging Client.'))
        report = self.env.ref('mysm_inventory.action_report_pif')
        return report.report_action(self.mapped('product_variant_id'), config=False)

class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_allergen(self):
        action = {
            'name': 'Allergen Composition ',
            'type': 'ir.actions.act_window',
            'res_model': 'mysm.allergen.composition',
            'view_mode': 'tree',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id}
        }
        return action

    def allergen_button(self):
        self.ensure_one()
        action = self.action_allergen()
        return action

    def generate_qr_code(self):
        self.ensure_one()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_current_page = '%s/web#id=%s&model=product.product&view_type=form' % (base_url, self.id)
        qr.add_data(url_current_page)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        return qr_image

    def _get_stock_picking(self):
        lines = self.env['stock.move.line'].search([
            ('product_id', '=', self.id),
            ('state', '=', 'done'),
        ])
        return lines.mapped('picking_id')

    def get_datetime_now_with_tz(self):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        now = now.astimezone(pytz.timezone(self.env.user.tz))
        return now.strftime('%d-%m-%Y %H:%M:%S')

class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    min_qty = fields.Float(string="MOQ")
    product_group = fields.Selection(related='product_tmpl_id.product_group')
