# models/account_payment_inherit.py
from odoo import models,fields,api
from werkzeug.urls import url_encode
from odoo.exceptions import UserError,ValidationError



class AccountMove(models.Model):
    _inherit = 'account.move'
  
    def _get_invoice_in_payment_state(self):
        # OVERRIDE to enable the 'in_payment' state on invoices.
        return 'paid'

