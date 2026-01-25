from odoo import models, api
from datetime import datetime


class LedgerAccountXlsx(models.AbstractModel):
    _name = 'report.ledger_report.ledger_account_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Ledger Account Excel Report'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate Excel report matching the ledger format"""
        
        # Define formats
        company_header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
        })
        
        company_info_format = workbook.add_format({
            'font_size': 9,
            'align': 'center',
            'valign': 'vcenter',
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'bg_color': '#E7E6E6',
        })
        
        cell_format = workbook.add_format({
            'font_size': 9,
            'valign': 'vcenter',
            'border': 1,
        })
        
        cell_center_format = workbook.add_format({
            'font_size': 9,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
        })
        
        number_format = workbook.add_format({
            'font_size': 9,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '#,##0.00',
        })
        
        bold_cell_format = workbook.add_format({
            'bold': True,
            'font_size': 9,
            'valign': 'vright',
            'border': 1,
        })

        bold_cell_center_format = workbook.add_format({
            'bold': True,
            'font_size': 9,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
        })        
        total_format = workbook.add_format({
            'bold': True,
            'font_size': 9,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '#,##0.00',
        })
        
        company = self.env.company
        
        for partner in partners:
            # Create sheet per partner
            sheet_name = f"{partner.name[:25]}"
            sheet = workbook.add_worksheet(sheet_name)
            
            # Set column widths
            sheet.set_column('A:A', 12)
            sheet.set_column('B:B', 35)
            sheet.set_column('C:C', 12)
            sheet.set_column('D:D', 12)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 15)
            
            row = 0
            
            # Company Header
            sheet.merge_range(row, 0, row, 5, company.name.upper(), company_header_format)
            row += 1
            
            # Company Address
            address = f"PO.BX {company.street or ''}, {company.city or ''} - {company.state_id.name if company.state_id else ''}"
            sheet.merge_range(row, 0, row, 5, address, company_info_format)
            row += 1
            
            # Company Phone
            if company.phone:
                sheet.merge_range(row, 0, row, 5, f"TEL: {company.phone}", company_info_format)
                row += 1
            
            # Company Email/Emirate
            if company.city:
                sheet.merge_range(row, 0, row, 5, f"Emirate: {company.city}", company_info_format)
                row += 1
            
            if partner.email:
                sheet.merge_range(row, 0, row, 5, f"E-Mail: {partner.email}", company_info_format)
                row += 1
            
            # TRN
            if company.vat:
                sheet.merge_range(row, 0, row, 5, f"TRN: {company.vat}", company_info_format)
                row += 1
            
            # Report Title
            row += 1
            sheet.merge_range(row, 0, row, 5, 'SALES', title_format)
            row += 1
            sheet.merge_range(row, 0, row, 5, 'Ledger Account', company_info_format)
            row += 1
            
            # Date Range
            if data and data.get('date_from'):
                # Convert string to date object if needed
                if isinstance(data['date_from'], str):
                    date_from = datetime.strptime(data['date_from'], '%Y-%m-%d').date()
                else:
                    date_from = data['date_from']
                
                if isinstance(data.get('date_to'), str):
                    date_to = datetime.strptime(data['date_to'], '%Y-%m-%d').date()
                else:
                    date_to = data.get('date_to')
                date_from_str = date_from.strftime('%d-%b-%y')
                date_to_str = date_to.strftime('%d-%b-%y') if date_to else date_from_str
                if date_to and date_to != date_from:
                    date_str = f"For {date_from_str} to {date_to_str}"
                else:
                    date_str = f"For {date_from_str}"
                
                sheet.merge_range(row, 0, row, 5, date_str, company_info_format)
                row += 1
            
            row += 1
            
            # Table Headers
            sheet.write(row, 0, 'Date', header_format)
            sheet.write(row, 1, 'Particulars', header_format)
            sheet.write(row, 2, 'Vch Type', header_format)
            sheet.write(row, 3, 'Vch No.', header_format)
            sheet.write(row, 4, 'Debit', header_format)
            sheet.write(row, 5, 'Credit', header_format)
            row += 1
            # Opening Balance
            opening_balance = self._get_opening_balance_xlsx(partner, data)
            sheet.write(row, 0, '', cell_format)  # Column A (Date)
            sheet.merge_range(row, 1, row, 4, '', cell_format)
            sheet.write(row, 1, 'Opening Balance', bold_cell_format)  # Column B (Particulars)
            sheet.write(row, 5, abs(opening_balance) if opening_balance != 0 else 0, total_format)  # Column F (Credit)
            row += 1
            # Transaction Lines
            moves = self._get_partner_moves_xlsx(partner, data)
            total_debit = 0
            total_credit = 0
            for move in moves:
                date_str = move['date'].strftime('%d-%b-%y') if hasattr(move['date'], 'strftime') else str(move['date'])
                sheet.write(row, 0, date_str, cell_format)
                sheet.write(row, 1, f"{move['particulars']}", cell_center_format)
                sheet.write(row, 2, move['vch_type'], cell_center_format)
                sheet.write(row, 3, move['vch_no'], cell_center_format)
                sheet.write(row, 4, '', number_format)
                sheet.write(row, 5, move['debit'] if move['debit'] else '', number_format)
                
                total_debit += move['debit']
                total_credit += move['credit']
                row += 1
            closing_balance = opening_balance + total_debit
            sheet.write(row, 0, '', cell_format)  # Column A (Date)
            sheet.merge_range(row, 1, row, 4, '', cell_format)
            sheet.write(row, 5, abs(closing_balance) if closing_balance != 0 else 0, number_format)  # Column F (Credit)
            row += 1
            # Closing Balance
            sheet.write(row, 0, '', cell_format)  # Column A (Date)
            sheet.merge_range(row, 1, row, 3, '', cell_format)
            sheet.write(row, 1, 'Closing Balance', bold_cell_format)  # Column B (Particulars)
            sheet.write(row, 4, abs(closing_balance) if closing_balance != 0 else 0, number_format)
            sheet.write(row, 5, '', cell_format)   # Column F (Credit)
            row += 1
            # Totals
            total_debit_col = abs(opening_balance) + total_debit
            total_credit_col = abs(opening_balance) + total_debit
            
            sheet.write(row, 0, '', cell_format)
            sheet.write(row, 1, '', cell_format)
            sheet.write(row, 2, '', cell_format)
            sheet.write(row, 3, '', cell_format)
            sheet.write(row, 4, total_debit_col if total_debit_col != 0 else '', total_format)
            sheet.write(row, 5, total_credit_col if total_credit_col != 0 else '', total_format)
    
    def _get_partner_moves_xlsx(self, partner, data):
        """Get partner moves for Excel"""
        domain = [
            ('partner_id', '=', partner.id),
            ('state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund'])
        ]
        
        if data:
            if data.get('date_from'):
                domain.append(('invoice_date', '>=', data['date_from']))
            if data.get('date_to'):
                domain.append(('invoice_date', '<=', data['date_to']))
        
        moves = self.env['account.move'].search(domain, order='invoice_date, id')
        
        move_lines = []
        for move in moves:
            for line in move.line_ids.filtered(
                lambda l: l.account_id.account_type == 'asset_receivable'
            ):
                move_lines.append({
                    'date': move.invoice_date or move.date,
                    'particulars': partner.name,
                    'vch_type': 'Sales',
                    'vch_no': move.name.split('/')[-1] if '/' in move.name else move.name,
                    'debit': line.debit,
                    'credit': line.credit,
                })
        
        return move_lines
    
    def _get_opening_balance_xlsx(self, partner, data):
        """Get opening balance for Excel"""
        domain = [
            ('partner_id', '=', partner.id),
            ('parent_state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('account_id.account_type', '=', 'asset_receivable')
        ]
        
        if data and data.get('date_from'):
            domain.append(('date', '<', data['date_from']))
        
        lines = self.env['account.move.line'].search(domain)
        return sum(lines.mapped('debit')) - sum(lines.mapped('credit'))
