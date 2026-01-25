
{
    'name': 'Metachem',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'This is for customization for Metachem',
    'description': """
        TThis id for customization for Metachem
    """,
    'author': 'Vasanth',
    'depends': ['base','account','hr'],
    'data': [
        'views/hr_employee_views.xml',
        'views/invoice_report.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'reports/invoice_report_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
