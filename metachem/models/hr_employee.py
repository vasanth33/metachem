from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    card_type = fields.Char()
    card_number = fields.Char()
    expiry_date = fields.Date()
    contract_type = fields.Char()
