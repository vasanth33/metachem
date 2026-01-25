from odoo import models, api

class LedgerAccountReport(models.AbstractModel):
    _name = 'report.ledger_report.ledger_account_document'
    _description = 'Ledger Account Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepare data for the ledger report"""
        from datetime import datetime
        
        if not data:
            data = {}
        
        # If docids is empty but we have partner_ids in data, use those
        if not docids and data.get('partner_ids'):
            docids = data['partner_ids']
        
        partners = self.env['res.partner'].browse(docids)
        
        # Convert string dates to date objects for PDF template
        date_from = None
        date_to = None
        if data.get('date_from'):
            if isinstance(data['date_from'], str):
                date_from = datetime.strptime(data['date_from'], '%Y-%m-%d').date()
            else:
                date_from = data['date_from']
        
        if data.get('date_to'):
            if isinstance(data['date_to'], str):
                date_to = datetime.strptime(data['date_to'], '%Y-%m-%d').date()
            else:
                date_to = data['date_to']
        
        report_data = []
        for partner in partners:
            moves = self._get_partner_moves(partner, data)
            opening_bal = self._get_opening_balance(partner, data)
            closing_bal = self._get_closing_balance(partner, data)
            
            # Always include partners from wizard even if no moves
            report_data.append({
                'partner': partner,
                'moves': moves,
                'opening_balance': opening_bal,
                'closing_balance': closing_bal,
            })
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': partners,
            'report_data': report_data,
            'company': self.env.company,
            'date_from': date_from,
            'date_to': date_to,
            'customer_type': data.get('customer_type', 'cash'),
        }
    
    def _get_partner_moves(self, partner, data):
        """Get all account moves for the partner"""
        domain = [
            ('partner_id', '=', partner.id),
            ('state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund'])
        ]
        
        if data.get('date_from'):
            domain.append(('invoice_date', '>=', data['date_from']))
        if data.get('date_to'):
            domain.append(('invoice_date', '<=', data['date_to']))
        
        moves = self.env['account.move'].search(domain, order='invoice_date, id')
        
        move_lines = []
        for move in moves:
            # Get receivable line
            for line in move.line_ids.filtered(
                lambda l: l.account_id.account_type == 'asset_receivable'
            ):
                move_lines.append({
                    'date': move.invoice_date or move.date,
                    'ref': move.name,
                    'particulars': partner.name,
                    'vch_type': 'Sales',
                    'vch_no': move.name.split('/')[-1] if '/' in move.name else move.name,
                    'debit': line.debit,
                    'credit': line.credit,
                })
        
        return move_lines
    
    def _get_opening_balance(self, partner, data):
        """Calculate opening balance"""
        domain = [
            ('partner_id', '=', partner.id),
            ('parent_state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('account_id.account_type', '=', 'asset_receivable')
        ]
        
        if data and data.get('date_from'):
            domain.append(('date', '<', data['date_from']))
        
        lines = self.env['account.move.line'].search(domain)
        balance = sum(lines.mapped('debit')) - sum(lines.mapped('credit'))
        return balance
    
    def _get_closing_balance(self, partner, data):
        """Calculate closing balance"""
        domain = [
            ('partner_id', '=', partner.id),
            ('parent_state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('account_id.account_type', '=', 'asset_receivable')
        ]
        
        if data and data.get('date_to'):
            domain.append(('date', '<=', data['date_to']))
        
        lines = self.env['account.move.line'].search(domain)
        balance = sum(lines.mapped('debit')) - sum(lines.mapped('credit'))
        return balance
