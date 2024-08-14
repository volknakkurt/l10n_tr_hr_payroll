# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.


from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'
    _description = 'Employee'

    military_service_status = fields.Selection([
        ('exempt', 'Exempt'),
        ('postponement', 'Postponement'),
        ('done', 'Done'),
        ('not_done', 'Not Done'),
    ], string='Military Service Status', default='done')
    discharge_date = fields.Date(string='Discharge Date')
    postponement_end_date = fields.Date(string='Postponement End Date')

    start_date_of_work = fields.Date(string='Start Date Of Work')
    social_security_status = fields.Selection([
        ('employer', 'Employer or Representative'),
        ('employee', 'Employee'),
        ('657-b-worker', 'Within the Scope of 657 SK(4/b)'),
        ('657-c-worker', 'Within the Scope of 657 SK(4/C)'),
        ('intern', 'Apprentices and Trainee Students'),
        ('others', 'Others'),

    ], string='Social Security Status', default='employer')

    incentive_code = fields.Selection([
        ('0000', '0000'),
        # ('04447', '04447'),
        ('04857', '04857 (Pasif)'),
        ('05510', '05510'),
        ('06645', '06645'),
        ('14857', '14857'),
        ('06111', '06111'),
        # ('15921', '15921'),
        ('16322', '16322'),
        ('25510', '25510'),
        # ('54857', '54857'),
        ('66486', '66486'),
    ], string='Incentives Number', default='0000')

    benefit_05510 = fields.Boolean(string='Take advantage of the 05510', default=True)
    benefit_06111 = fields.Boolean(string='STake advantage of the 06111', default=True)
    incentive_start_date = fields.Date(string="Incentives Start Date")
    incentive_end_date = fields.Date(string="Incentives End Date", required=False)
    incentive_days = fields.Integer(string="Incentives Time (days)", required=False)

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)

    search_lines = fields.Many2many('hr.employee.search')


