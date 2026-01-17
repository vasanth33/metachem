from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_print_dot_matrix_receipt(self):
        """
        Print invoice receipt for dot matrix printer on pre-printed paper
        """
        self.ensure_one()
        return self.env.ref('dot_matrix_invoice_printer.action_report_dot_matrix_invoice').report_action(self)