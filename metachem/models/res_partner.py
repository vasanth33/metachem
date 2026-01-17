from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    date_of_registration = fields.Date('Date of VAT Registration')
    trn = fields.Char(string='TRN')
    registration_type =  fields.Selection(
        [
            ("registered", "Registered"),
            ("unregistered", "Unregistered"),
        ],
        string="Registration Type",
    )
    
