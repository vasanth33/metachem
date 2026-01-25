from odoo import models, fields, api
from odoo.exceptions import UserError

class LedgerReportWizard(models.TransientModel):
    _name = 'ledger.report.wizard'
    _description = 'Ledger Report Wizard'
    
    date_from = fields.Date(
        string='Date From',
        required=True,
        default=fields.Date.context_today
    )
    date_to = fields.Date(
        string='Date To',
        required=True,
        default=fields.Date.context_today
    )
    customer_type = fields.Selection([
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ], string='Customer Type', required=True, default='cash')
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from > wizard.date_to:
                raise UserError("Date From cannot be later than Date To!")
    
    def _get_partners(self):
        """Get partners based on selection"""
        domain = []
        
        # Filter by customer type
        if self.customer_type != 'all':
            domain.append(('customer_type', '=', self.customer_type))
        
        # Filter by specific partners if selected
        domain.append(('customer_rank', '>', 0))
        
        partners = self.env['res.partner'].search(domain)
        
        # Filter partners that have transactions in date range
        partners_with_transactions = self.env['res.partner']
        for partner in partners:
            move_count = self.env['account.move'].search_count([
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
            ])
            if move_count > 0:
                partners_with_transactions |= partner
        
        return partners_with_transactions
    
    def action_print_pdf(self):
        """Generate PDF Report"""
        partners = self._get_partners()
        
        if not partners:
            raise UserError("No customers found with transactions in the selected date range!")
        
        data = {
            'date_from': str(self.date_from),
            'date_to': str(self.date_to),
            'customer_type': self.customer_type,
            'partner_ids': partners.ids,  # Pass partner IDs in data
        }
        
        # Pass partners.ids as docids
        return self.env.ref('ledger_report.action_report_ledger_pdf').report_action(
            partners.ids, data=data
        )
            
    def action_print_excel(self):
        """Generate Excel Report"""
        partners = self._get_partners()
        
        if not partners:
            raise UserError("No customers found with transactions in the selected date range!")
        
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_type': self.customer_type,
        }
        
        return self.env.ref('ledger_report.action_report_ledger_xlsx').report_action(
            partners, data=data
        )
