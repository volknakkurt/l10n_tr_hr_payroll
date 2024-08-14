# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.


from odoo import api, fields, models


class HrRuleInput(models.Model):
    _inherit = 'hr.payslip.input'
    _description = 'Salary Rule Input'

    input_id = fields.Many2one('hr.salary.rule', string='Salary Rule Input')
