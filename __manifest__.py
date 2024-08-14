# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.

{
    "name": "Turkey Localization Payslip",
    "version": "17.0.1.0.1",
    "author": "Volkan",
    'summary': 'Turkey Payslip For Odoo 17',
    'category': 'Human Resources/Payroll',
    "license": "AGPL-3",
    "complexity": "normal",
    "depends": [
        'hr_contract',
        'hr_payroll',
        'hr_holidays',],
    "data": [
        'security/ir.model.access.csv',
        'data/hr_payroll_rules.xml',
        'views/hr_contract_views.xml',
        'report/report_overriden_payslip_template_new.xml',
        'report/report_summary_templates.xml',
        'views/hr_employee_views.xml',
        'report/hr_payroll_report.xml',
        'views/hr_payslip_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "auto_install": False,
    "installable": True,
}
