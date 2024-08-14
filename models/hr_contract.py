# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.

from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    type_salary = fields.Selection([
        ('net', 'Net'),
        ('gross', 'Gross'),
    ], string='Salary Type', default='gross')

    disabled_degree = fields.Selection([
        ('not_disabled', 'Engelsiz'),
        ('disabled_1', '1. Derece Engelli'),
        ('disabled_2', '2. Derece Engelli'),
        ('disabled_3', '3. Derece Engelli'),
    ], string='Disabled Status', default='not_disabled')

    previous_cumulative_tax_base = fields.Monetary(string='Previous Cumulative Tax Base', default=0.0)
    
    # Added for getting minimum salary automatically
    is_minimum_wage = fields.Boolean(string="Minimum Wage", default=False)
    wage = fields.Monetary(string="Wage", )

    @api.onchange('is_minimum_wage', 'type_salary', "wage")
    def _get_min_wage_automatically(self):
        settings_dict = {}
        ICPSudo = self.env['ir.config_parameter'].sudo()
        settings_dict['gross_minimum_wage'] = ICPSudo.get_param('l10n_tr_hr_payroll.gross_minimum_wage')
        settings_dict['net_minimum_wage'] = ICPSudo.get_param('l10n_tr_hr_payroll.net_minimum_wage')

        if self.type_salary == 'net' and self.is_minimum_wage:
            self.wage = settings_dict['net_minimum_wage']
        elif self.type_salary == 'gross' and self.is_minimum_wage:
            self.wage = settings_dict['gross_minimum_wage']
        else:
            self.wage = self.wage

    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by hierarchy (parent=False first,
                 then first level children and so on) and without duplicate
        """
        structures = self.mapped('struct_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure()))