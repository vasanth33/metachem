{
    'name': 'Dot Matrix Invoice Printer',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Print invoices on pre-printed paper using dot matrix printer',
    'description': """
        This module allows printing invoices on pre-printed paper (28cm x 25cm)
        using a dot matrix printer. It adds a "Print Receipt" button to invoices.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
        'report/report_paperformat.xml',
        'report/dot_matrix_invoice_report.xml',
        'report/dot_matrix_invoice_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}