# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class HrEmployeeSummary(models.Model):
    _name = 'hr.employee.search'
    _description = 'Employee Search'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
    date_from = fields.Date(string='Summary Start Date', required=True)
    date_to = fields.Date(string='Summary End Date', compute='_compute_date_to', readonly=True)
    month = fields.Char(string='Month', compute='_compute_month', readonly=True)

    @api.onchange('date_from')
    def onchange_date_from(self):
        if self.date_from:
            self.date_from = self.date_from.replace(day=1)

    @api.depends('date_from')
    def _compute_date_to(self):
        for record in self:
            if record.date_from:
                record.date_to = record.date_from + relativedelta(months=1, day=1, days=-1)
            else:
                record.date_to = False

    @api.depends('date_from')
    def _compute_month(self):
        for record in self:
            if record.date_from:
                record.month = record.date_from.strftime('%B')
            else:
                record.month = False

    def generate_report(self):
        self.ensure_one()
        [data] = self.read()
        data['emp'] = self.env.context.get('active_ids', [])
        datas = {
            'ids': [],
            'model': 'hr.employee.search',
            'form': data
        }
        return self.env.ref('l10n_tr_hr_payroll.hr_employee_summary_report').report_action(
            self.env['hr.employee'].browse(data['emp']), data=datas)
