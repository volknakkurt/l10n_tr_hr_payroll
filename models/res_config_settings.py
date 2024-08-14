# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gross_minimum_wage = fields.Float(string='Current Gross Minimum Wage')
    net_minimum_wage = fields.Float(string='Current Net Minimum Wage')
    ssi_ceiling_amount = fields.Float(string='SSI Ceiling Amount')
    ssi_worker_prim_rate = fields.Float(string='SSI Worker Prim Rate', digits=(16, 3))
    ssi_unemployment_worker_rate = fields.Float(string='SSI Unemployment Worker Rate', digits=(16, 3))
    ssi_worker_retired_rate = fields.Float(string='SSI Worker Retired Rate', digits=(16, 3))
    ssi_employer_prim_rate = fields.Float(string='SSI Employer Prim Rate', digits=(16, 3))
    ssi_unemployment_employer_rate = fields.Float(string='SSI Unemployment Employer Rate', digits=(16, 3))
    ssi_employer_retired_rate = fields.Float(string='SSI Employer Retired Rate', digits=(16, 3))
    stump_tax_rate = fields.Float(string='Stamp Tax Rate', digits=(16, 5))
    extra_shift_rate = fields.Float(string='Extra Shift Rate', digits=(16, 3))
    overtime_shift_rate = fields.Float(string='Overtime Shift Rate', digits=(16, 3))
    holiday_shift_rate = fields.Float(string='Holiday Shift Rate', digits=(16, 3))
    food_allowance_rate = fields.Float(string='Food Allowance Rate', digits=(16, 3))
    family_allowance_rate = fields.Float(string='Family Allowance Rate', digits=(16, 3))
    individual_pension_rate = fields.Float(string='Individual Pension Rate', digits=(16, 3))
    first_part_tax = fields.Float(string='First Tax Ceiling Price')
    second_part_tax = fields.Float(string='Second Tax Ceiling Price')
    third_part_tax = fields.Float(string='Third Tax Ceiling Price')
    fourth_part_tax = fields.Float(string='Fourth Tax Ceiling Price')
    first_part_tax_ratio = fields.Float(string='First Tax Bracket Rate')
    second_part_tax_ratio = fields.Float(string='Second Tax Bracket Rate')
    third_part_tax_ratio = fields.Float(string='Third Tax Bracket Rate')
    fourth_part_tax_ratio = fields.Float(string='Fourth Tax Bracket Rate')
    fifth_part_tax_ratio = fields.Float(string='Fifth Tax Bracket Rate')
    first_degree_disabled_discount = fields.Float(string='1. Degree Disabled Discount')
    second_degree_disabled_discount = fields.Float(string='2. Degree Disabled Discount')
    third_degree_disabled_discount = fields.Float(string='3. Degree Disabled Discount')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.first_degree_disabled_discount',
                                                  self.first_degree_disabled_discount)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.second_degree_disabled_discount',
                                                  self.second_degree_disabled_discount)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.third_degree_disabled_discount',
                                                  self.third_degree_disabled_discount)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_worker_prim_rate', self.ssi_worker_prim_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_worker_retired_rate',
                                                  self.ssi_worker_retired_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_unemployment_worker_rate',
                                                  self.ssi_unemployment_worker_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_unemployment_employer_rate',
                                                  self.ssi_unemployment_employer_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_employer_prim_rate',
                                                  self.ssi_employer_prim_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.gross_minimum_wage', self.gross_minimum_wage)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.net_minimum_wage', self.net_minimum_wage)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.stump_tax_rate', self.stump_tax_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.extra_shift_rate', self.extra_shift_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.overtime_shift_rate', self.overtime_shift_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.holiday_shift_rate', self.holiday_shift_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.food_allowance_rate',
                                                  self.food_allowance_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.family_allowance_rate',
                                                  self.family_allowance_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.individual_pension_rate',
                                                  self.individual_pension_rate)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_ceiling_amount', self.ssi_ceiling_amount)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.first_part_tax', self.first_part_tax)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.second_part_tax', self.second_part_tax)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.third_part_tax', self.third_part_tax)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.fourth_part_tax', self.fourth_part_tax)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.first_part_tax_ratio', self.first_part_tax_ratio)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.second_part_tax_ratio',
                                                  self.second_part_tax_ratio)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.third_part_tax_ratio', self.third_part_tax_ratio)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.fourth_part_tax_ratio',
                                                  self.fourth_part_tax_ratio)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.fifth_part_tax_ratio', self.fifth_part_tax_ratio)
        self.env['ir.config_parameter'].set_param('l10n_tr_hr_payroll.ssi_employer_retired_rate',
                                                  self.ssi_employer_retired_rate)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        first_degree_disabled_discount = ICPSudo.get_param('l10n_tr_hr_payroll.first_degree_disabled_discount')
        second_degree_disabled_discount = ICPSudo.get_param('l10n_tr_hr_payroll.second_degree_disabled_discount')
        third_degree_disabled_discount = ICPSudo.get_param('l10n_tr_hr_payroll.third_degree_disabled_discount')
        ssi_worker_prim_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_worker_prim_rate')
        ssi_worker_retired_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_worker_retired_rate')
        ssi_unemployment_worker_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_unemployment_worker_rate')
        ssi_unemployment_employer_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_unemployment_employer_rate')
        ssi_employer_prim_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_employer_prim_rate')
        gross_minimum_wage = ICPSudo.get_param('l10n_tr_hr_payroll.gross_minimum_wage')
        net_minimum_wage = ICPSudo.get_param('l10n_tr_hr_payroll.net_minimum_wage')
        stump_tax_rate = ICPSudo.get_param('l10n_tr_hr_payroll.stump_tax_rate')
        extra_shift_rate = ICPSudo.get_param('l10n_tr_hr_payroll.extra_shift_rate')
        overtime_shift_rate = ICPSudo.get_param('l10n_tr_hr_payroll.overtime_shift_rate')
        holiday_shift_rate = ICPSudo.get_param('l10n_tr_hr_payroll.holiday_shift_rate')
        food_allowance_rate = ICPSudo.get_param('l10n_tr_hr_payroll.food_allowance_rate')
        family_allowance_rate = ICPSudo.get_param('l10n_tr_hr_payroll.family_allowance_rate')
        individual_pension_rate = ICPSudo.get_param('l10n_tr_hr_payroll.individual_pension_rate')
        ssi_ceiling_amount = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_ceiling_amount')
        first_part_tax = ICPSudo.get_param('l10n_tr_hr_payroll.first_part_tax')
        second_part_tax = ICPSudo.get_param('l10n_tr_hr_payroll.second_part_tax')
        third_part_tax = ICPSudo.get_param('l10n_tr_hr_payroll.third_part_tax')
        fourth_part_tax = ICPSudo.get_param('l10n_tr_hr_payroll.fourth_part_tax')
        first_part_tax_ratio = ICPSudo.get_param('l10n_tr_hr_payroll.first_part_tax_ratio')
        second_part_tax_ratio = ICPSudo.get_param('l10n_tr_hr_payroll.second_part_tax_ratio')
        third_part_tax_ratio = ICPSudo.get_param('l10n_tr_hr_payroll.third_part_tax_ratio')
        fourth_part_tax_ratio = ICPSudo.get_param('l10n_tr_hr_payroll.fourth_part_tax_ratio')
        fifth_part_tax_ratio = ICPSudo.get_param('l10n_tr_hr_payroll.fifth_part_tax_ratio')
        ssi_employer_retired_rate = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_employer_retired_rate')
        res.update(
            first_degree_disabled_discount=first_degree_disabled_discount,
            second_degree_disabled_discount=second_degree_disabled_discount,
            third_degree_disabled_discount=third_degree_disabled_discount,
            ssi_worker_prim_rate=ssi_worker_prim_rate,
            ssi_worker_retired_rate=ssi_worker_retired_rate,
            ssi_unemployment_worker_rate=ssi_unemployment_worker_rate,
            ssi_unemployment_employer_rate=ssi_unemployment_employer_rate,
            ssi_employer_prim_rate=ssi_employer_prim_rate,
            gross_minimum_wage=gross_minimum_wage,
            net_minimum_wage=net_minimum_wage,
            stump_tax_rate=stump_tax_rate,
            extra_shift_rate=extra_shift_rate,
            overtime_shift_rate=overtime_shift_rate,
            holiday_shift_rate=holiday_shift_rate,
            food_allowance_rate=food_allowance_rate,
            family_allowance_rate=family_allowance_rate,
            individual_pension_rate=individual_pension_rate,
            ssi_ceiling_amount=ssi_ceiling_amount,
            first_part_tax=first_part_tax,
            second_part_tax=second_part_tax,
            third_part_tax=third_part_tax,
            fourth_part_tax=fourth_part_tax,
            first_part_tax_ratio=first_part_tax_ratio,
            second_part_tax_ratio=second_part_tax_ratio,
            third_part_tax_ratio=third_part_tax_ratio,
            fourth_part_tax_ratio=fourth_part_tax_ratio,
            fifth_part_tax_ratio=fifth_part_tax_ratio,
            ssi_employer_retired_rate=ssi_employer_retired_rate,
        )
        return res
