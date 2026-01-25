from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    customer_type = fields.Selection([
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ], string='Customer Type', required=True, default='cash',
       help="Specify whether this customer is a Cash or Credit customer")
    
    @api.model
    def create(self, vals):
        """Ensure customer_type is set on creation"""
        if 'customer_type' not in vals:
            vals['customer_type'] = 'cash'
        return super(ResPartner, self).create(vals)
