{
    'name': 'Ledger Account Report',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Ledger Account Statement with PDF and Excel Export',
    'depends': ['base', 'account', 'report_xlsx','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'wizard/ledger_report_wizard_views.xml',
        'views/report_template.xml',
        'report/ledger_report.xml',
    ],
    'installable': True,
    'application': False,
}