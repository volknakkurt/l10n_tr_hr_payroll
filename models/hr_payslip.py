# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.


from odoo import api, fields, models, tools, _
from datetime import date, datetime, time
import babel
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

initialInputs = [{
    'name': 'Food Allowance',
    'code': 'food_allowance',
    'contract_id': 0,
}, {
    'name': 'Food Days',
    'code': 'food_days_input',
    'contract_id': 0,
}, {
    'name': 'Road Allowance',
    'code': 'road_allowance',
    'contract_id': 0,
}, {
    'name': 'Family Allowance',
    'code': 'family_allowance',
    'contract_id': 0,
}, {
    'name': 'Child Allowance',
    'code': 'child_allowance',
    'contract_id': 0,
}, {
    'name': 'Marriage Allowance',
    'code': 'marriage_allowance',
    'contract_id': 0,
}, {
    'name': 'Birth Allowance',
    'code': 'birth_allowance',
    'contract_id': 0,
}, {
    'name': 'Death Allowance',
    'code': 'death_allowance',
    'contract_id': 0,
}, {
    'name': 'Prim Allowance',
    'code': 'prim_allowance',
    'contract_id': 0,
}, {
    'name': 'Holiday Allowance',
    'code': 'holiday_allowance',
    'contract_id': 0,
}, {
    'name': 'Bonus Allowance',
    'code': 'bonus_allowance',
    'contract_id': 0,
}, {
    'name': 'Fuel Allowance',
    'code': 'fuel_allowance',
    'contract_id': 0,
}, {
    'name': 'Attendance Allowance',
    'code': 'attendance_allowance',
    'contract_id': 0,
}, {
    'name': 'Syndicate Deductions',
    'code': 'syndicate_deductions',
    'contract_id': 0,
}, {
    'name': 'Execution Deduction',
    'code': 'execution_deductions',
    'contract_id': 0,
}, {
    'name': 'Advance Deductions',
    'code': 'advance_deductions',
    'contract_id': 0,
}, {
    'name': 'Notice Allowance',
    'code': 'notice_allowance',
    'contract_id': 0,
}, {
    'name': 'Severance Allowance',
    'code': 'severance_allowance',
    'contract_id': 0,
}, ]

worked_days_input = [{
    'name': 'Regular Shift',
    'sequence': 1,
    'code': 'regular_shift_basic',
    'number_of_days': 22,
    'number_of_hours': 165,
    'contract_id': 1,
}, {
    'name': 'Weekend Holiday',
    'sequence': 2,
    'code': 'weekend_holiday_basic',
    'number_of_days': 8,
    'number_of_hours': 60,
    'contract_id': 1,
}, {
    'name': 'National Holiday',
    'sequence': 3,
    'code': 'national_holiday_basic',
    'number_of_days': 0,
    'number_of_hours': 0,
    'contract_id': 1,
}, {
    'name': 'Extra Shift',
    'sequence': 6,
    'code': 'extra_shift_basic',
    'number_of_days': 0,
    'number_of_hours': 0,
    'contract_id': 1,
}, {
    'name': 'Overtime Shift',
    'sequence': 6,
    'code': 'overtime_shift_basic',
    'number_of_days': 0,
    'number_of_hours': 0,
    'contract_id': 1,
}, {
    'name': 'Holiday Shift',
    'sequence': 7,
    'code': 'holiday_shift_basic',
    'number_of_days': 0,
    'number_of_hours': 0,
    'contract_id': 1,
},
    # {
    #     'name': 'Free vacation',
    #     'sequence': 5,
    #     'code': 'missing_day_basic',
    #     'number_of_days': 0,
    #     'number_of_hours': 0,
    #     'contract_id': 1,
    # }, {
    #     'name': 'Paid vacation',
    #     'sequence': 4,
    #     'code': 'paid_vacation_basic',
    #     'number_of_days': 0,
    #     'number_of_hours': 0,
    #     'contract_id': 1,
    # },
]


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    payslip_period = fields.Char(string='Payslip Period', compute='_compute_payslip_period', readonly=True)

    @api.depends('date_from')
    def _compute_payslip_period(self):
        for record in self:
            if record.date_from:
                record.payslip_period = f"{record.date_from.strftime('%B')} {record.date_from.year}"
                month_translation = {
                    'January': 'Ocak',
                    'February': 'Şubat',
                    'March': 'Mart',
                    'April': 'Nisan',
                    'May': 'Mayıs',
                    'June': 'Haziran',
                    'July': 'Temmuz',
                    'August': 'Ağustos',
                    'September': 'Eylül',
                    'October': 'Ekim',
                    'November': 'Kasım',
                    'December': 'Aralık'
                }
                record.payslip_period = month_translation.get(record.date_from.strftime('%B'),
                                                              record.date_from.strftime(
                                                                  '%B')) + f" {record.date_from.year}"
            else:
                record.payslip_period = False

    # İsmini değiştiriyor
    def _compute_salary_slip_name(self):
        """ Compute the name of the salary slip """
        if not (self.employee_id and self.date_from and self.date_to):
            return
        employee = self.employee_id
        date_from = self.date_from
        locale = self.env.context.get('lang') or 'en_US'
        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        self.name = _('Salary Slip of %s for %s') % (
            employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

    # Çalışma günleri girişlerini çekiyor
    # @api.model
    # def _get_worked_day_lines(self):
    #     self.struct_id.use_worked_day_lines = True
    #     res = super(HrPayslip, self)._get_worked_day_lines()
    #     return res

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        self.ensure_one()
        self._compute_salary_slip_name()

    @api.model
    def get_payslip_lines(self, payslip_id):

        def _sum_salary_rule_category(local_dict, category, amount):
            if category.parent_id:
                local_dict = _sum_salary_rule_category(local_dict, category.parent_id, amount)
            local_dict['categories'].dict[category.code] = category.code in local_dict['categories'].dict and \
                                                           local_dict['categories'].dict[
                                                               category.code] + amount or amount
            return local_dict

        class BrowsableObject(object):
            def __init__(self, employee_id, dict, env):
                self.employee_id = employee_id
                self.dict = dict
                self.env = env

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                        SELECT sum(amount) as sum
                        FROM hr_payslip as hp, hr_payslip_input as pi
                        WHERE hp.employee_id = %s AND hp.state = 'done'
                        AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()[0] or 0.0

        class Settings(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                           SELECT sum(amount) as sum
                           FROM hr_payslip as hp, hr_payslip_input as pi
                           WHERE hp.employee_id = %s AND hp.state = 'done'
                           AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()[0] or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                        SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours
                        FROM hr_payslip as hp, hr_payslip_worked_days as pi
                        WHERE hp.employee_id = %s AND hp.state = 'done'
                        AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)
                                FROM hr_payslip as hp, hr_payslip_line as pl
                                WHERE hp.employee_id = %s AND hp.state = 'done'
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                res = self.env.cr.fetchone()
                return res and res[0] or 0.0

        # we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules_dict = {}
        settings_dict = {}
        worked_days_dict = {}
        inputs_dict = {}
        blacklist = []

        # Get payslip, payslip in worked days lines and input lines
        payslip = self.env['hr.payslip'].browse(payslip_id)
        for worked_days_line in payslip.worked_days_line_ids:
            worked_days_dict[worked_days_line.code] = worked_days_line

        for input_line in payslip.input_line_ids:
            inputs_dict[input_line.code] = input_line

        # Get payroll parameters from settings and set them in settings_dict dictionary
        ICPSudo = self.env['ir.config_parameter'].sudo()
        settings_dict['first_degree_disabled_discount'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.first_degree_disabled_discount')
        settings_dict['second_degree_disabled_discount'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.second_degree_disabled_discount')
        settings_dict['third_degree_disabled_discount'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.third_degree_disabled_discount')
        settings_dict['ssi_worker_prim_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_worker_prim_rate')
        settings_dict['ssi_worker_retired_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_worker_retired_rate')
        settings_dict['ssi_unemployment_worker_rate'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.ssi_unemployment_worker_rate')
        settings_dict['ssi_unemployment_employer_rate'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.ssi_unemployment_employer_rate')
        settings_dict['ssi_employer_prim_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_employer_prim_rate')
        settings_dict['gross_minimum_wage'] = ICPSudo.get_param('l10n_tr_hr_payroll.gross_minimum_wage')
        settings_dict['net_minimum_wage'] = ICPSudo.get_param('l10n_tr_hr_payroll.net_minimum_wage')
        settings_dict['stump_tax_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.stump_tax_rate')
        settings_dict['extra_shift_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.extra_shift_rate')
        settings_dict['overtime_shift_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.overtime_shift_rate')
        settings_dict['holiday_shift_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.holiday_shift_rate')
        settings_dict['food_allowance_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.food_allowance_rate')
        settings_dict['family_allowance_rate'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.family_allowance_rate')
        settings_dict['individual_pension_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.individual_pension_rate')
        settings_dict['ssi_ceiling_amount'] = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_ceiling_amount')
        settings_dict['first_part_tax'] = ICPSudo.get_param('l10n_tr_hr_payroll.first_part_tax')
        settings_dict['second_part_tax'] = ICPSudo.get_param('l10n_tr_hr_payroll.second_part_tax')
        settings_dict['third_part_tax'] = ICPSudo.get_param('l10n_tr_hr_payroll.third_part_tax')
        settings_dict['fourth_part_tax'] = ICPSudo.get_param('l10n_tr_hr_payroll.fourth_part_tax')
        settings_dict['first_part_tax_ratio'] = ICPSudo.get_param('l10n_tr_hr_payroll.first_part_tax_ratio')
        settings_dict['second_part_tax_ratio'] = ICPSudo.get_param('l10n_tr_hr_payroll.second_part_tax_ratio')
        settings_dict['third_part_tax_ratio'] = ICPSudo.get_param('l10n_tr_hr_payroll.third_part_tax_ratio')
        settings_dict['fourth_part_tax_ratio'] = ICPSudo.get_param('l10n_tr_hr_payroll.fourth_part_tax_ratio')
        settings_dict['fifth_part_tax_ratio'] = ICPSudo.get_param('l10n_tr_hr_payroll.fifth_part_tax_ratio')
        settings_dict['first_degree_disabled_addition'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.first_degree_disabled_addition')
        settings_dict['second_degree_disabled_addition'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.second_degree_disabled_addition')
        settings_dict['third_degree_disabled_addition'] = ICPSudo.get_param(
            'l10n_tr_hr_payroll.third_degree_disabled_addition')
        settings_dict['ssi_employer_retired_rate'] = ICPSudo.get_param('l10n_tr_hr_payroll.ssi_employer_retired_rate')

        categories = BrowsableObject(payslip.employee_id.id, {}, self.env)
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        worked_days = WorkedDays(payslip.employee_id.id, worked_days_dict, self.env)
        payslips = Payslips(payslip.employee_id.id, payslip, self.env)
        rules = BrowsableObject(payslip.employee_id.id, rules_dict, self.env)
        settings = Settings(payslip.employee_id.id, settings_dict, self.env)

        base_local_dict = {'categories': categories, 'rules': rules, 'payslip': payslips, 'worked_days': worked_days,
                           'inputs': inputs, 'settings': settings}

        structure_id = self.struct_id.id

        rule_ids = self.env['hr.payroll.structure'].browse(structure_id).get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        sorted_rules = self.env['hr.salary.rule'].browse(sorted_rule_ids)

        contract = self.contract_id
        local_dict = dict(base_local_dict, employee=self.employee_id, contract=self.contract_id)
        newGross = 0
        net_amount = 0
        if contract.type_salary == 'net':

            workedHours = worked_days_dict['regular_shift_basic'].number_of_hours if worked_days_dict.get(
                'regular_shift_basic') else 0
            workedHolidaysHours = worked_days_dict['weekend_holiday_basic'].number_of_hours if worked_days_dict.get(
                'weekend_holiday_basic') else 0
            workedHolidays_1Hours = worked_days_dict[
                'national_holiday_basic'].number_of_hours if worked_days_dict.get('national_holiday_basic') else 0
            workedOffHours = worked_days_dict['paid_vacation_basic'].number_of_hours if worked_days_dict.get(
                'paid_vacation_basic') else 0
            extraHours = worked_days_dict['extra_shift_basic'].number_of_hours if worked_days_dict.get(
                'extra_shift_basic') else 0
            nightHours = worked_days_dict['overtime_shift_basic'].number_of_hours if worked_days_dict.get(
                'overtime_shift_basic') else 0
            holidayHours = worked_days_dict['holiday_shift'].number_of_hours if worked_days_dict.get(
                'holiday_shift') else 0

            dailyHours = contract.resource_calendar_id.hours_per_day
            aHourPrice = contract.wage / 225

            others = 0
            if inputs_dict.get('bonus_allowance'):
                others += inputs_dict['bonus_allowance'].amount
            if inputs_dict.get('prim_allowance'):
                others += inputs_dict['prim_allowance'].amount
            if inputs_dict.get('birth_allowance'):
                others += inputs_dict['birth_allowance'].amount
            if inputs_dict.get('death_allowance'):
                others += inputs_dict['death_allowance'].amount
            if inputs_dict.get('marriage_allowance'):
                others += inputs_dict['marriage_allowance'].amount
            if inputs_dict.get('attendance_allowance'):
                others += inputs_dict['attendance_allowance'].amount
            if inputs_dict.get('holiday_allowance'):
                others += inputs_dict['holiday_allowance'].amount
            if inputs_dict.get('fuel_allowance'):
                others += inputs_dict['fuel_allowance'].amount
            if inputs_dict.get('food_allowance'):
                others += inputs_dict['food_allowance'].amount
            if inputs_dict.get('road_allowance'):
                others += inputs_dict['road_allowance'].amount
            if inputs_dict.get('child_allowance'):
                others += inputs_dict['child_allowance'].amount
            if inputs_dict.get('family_allowance'):
                others += inputs_dict['family_allowance'].amount
            if inputs_dict.get('severance_allowance'):
                others += inputs_dict['severance_allowance'].amount
            if inputs_dict.get('notice_allowance'):
                others += inputs_dict['notice_allowance'].amount

            '''if contract.disabled_degree == "disabled_1":
                others += float(settings_dict['first_degree_disabled_addition'])
            if contract.disabled_degree == "disabled_2":
                others += float(settings_dict['second_degree_disabled_addition'])
            if contract.disabled_degree == "disabled_3":
                others += float(settings_dict['third_degree_disabled_addition'])'''

            if inputs_dict.get('advance_deductions'):
                others -= inputs_dict['advance_deductions'].amount
            if inputs_dict.get('execution_deductions'):
                others -= inputs_dict['execution_deductions'].amount
            if inputs_dict.get('syndicate_deductions'):
                others -= inputs_dict['syndicate_deductions'].amount

            newNet = (
                             workedHours + workedHolidays_1Hours + workedHolidaysHours + workedOffHours) * aHourPrice + float(
                settings_dict['extra_shift_rate']) * extraHours * aHourPrice + float(
                settings_dict['overtime_shift_rate']) * nightHours * aHourPrice + float(
                settings_dict['holiday_shift_rate']) * holidayHours * aHourPrice + others
            newGross = newNet * 2 - 2 * others

            i = 0
            ratioOfDecrease = contract.wage
            if newGross == 0 and newNet == 0:
                newGross = 1
                net_amount = 1
            _logger.info('newGross :::' + str(newGross) + 'newNet :::' + str(newNet))
            while (newNet != net_amount) and i < 155:
                ek = others
                i = i + 1
                bes = 0
                for rule in sorted_rules:
                    key = rule.code + '-' + str(contract.id)
                    local_dict['result'] = None
                    local_dict['result_qty'] = 1.0
                    local_dict['result_rate'] = 100
                    # check if the rule can be applied
                    if rule._satisfy_condition(local_dict) and rule.id not in blacklist:
                        # compute the amount of the rule
                        amount, qty, rate = rule._compute_rule(local_dict)

                        # check if there is already a rule computed with that code
                        previous_amount = rule.code in local_dict and local_dict[rule.code] or 0.0
                        # set/overwrite the amount computed for this rule in the local_dict
                        tot_rule = contract.company_id.currency_id.round(amount * qty * rate / 100.0)
                        if rule.code == 'amount_gross':
                            amount = newGross
                            tot_rule = newGross
                            _logger.info('newGross :::' + str(amount))

                        local_dict[rule.code] = tot_rule
                        rules_dict[rule.code] = rule
                        if rule.code == 'amount_net':
                            net_amount = tot_rule
                            amount = amount
                            _logger.info('net_amount :::' + str(net_amount))
                            _logger.info('newNet :::' + str(newNet))
                            _logger.info('ratioOfDecrease :::' + str(ratioOfDecrease))
                            ratioOfDecrease = (net_amount - newNet) / 2
                            if ratioOfDecrease < 0:
                                ratioOfDecrease = ratioOfDecrease * -1
                            if ratioOfDecrease < 0.001:
                                newNet = round(newNet, 2)
                            if net_amount > newNet:
                                newGross = newGross - ratioOfDecrease
                            elif net_amount < newNet:
                                newGross = newGross + ratioOfDecrease
                            '''
                            fark = net_amount-newNet
                            if fark<0:
                                fark *=-1
                                i = 5000
                            oran = fark/newNet*100
                            _logger.info('fark :::' + str(fark) + '   oran :::' + str(oran))
                            if oran>100:
                                ratioOfDecrease = 0.1
                            elif oran>50:
                                ratioOfDecrease = 0.09
                            elif oran>20:
                                ratioOfDecrease = 0.085
                            elif oran>10:
                                ratioOfDecrease = 0.008
                            elif oran>8:
                                ratioOfDecrease = 0.007
                            elif oran>7:
                                ratioOfDecrease = 0.006
                            elif oran>6:
                                ratioOfDecrease = 0.005
                            elif oran>5:
                                ratioOfDecrease = 0.004
                            elif oran>4:
                                ratioOfDecrease = 0.003
                            elif oran>3:
                                ratioOfDecrease = 0.0002
                            elif oran>2:
                                ratioOfDecrease = 0.0001
                            elif oran>1:
                                ratioOfDecrease = 0.00005
                                '''

                        # sum the amount for its salary category
                        local_dict = _sum_salary_rule_category(local_dict, rule.category_id,
                                                               tot_rule - previous_amount)
                        # create/overwrite the rule in the temporary results
                        result_dict[key] = {
                            'salary_rule_id': rule.id,
                            'contract_id': contract.id,
                            'name': rule.name,
                            'code': rule.code,
                            'category_id': rule.category_id.id,
                            'sequence': rule.sequence,
                            'appears_on_payslip': rule.appears_on_payslip,
                            'amount_select': rule.amount_select,
                            'amount_fix': rule.amount_fix,
                            'amount_percentage': rule.amount_percentage,
                            'amount': amount,
                            'employee_id': contract.employee_id.id,
                            'rate': rate,
                        }


                    else:
                        # blacklist this rule and its children
                        blacklist += [id for id, seq in rule._recursive_search_of_rules()]

                # result_dict.pop("amount_gross-" + str(contract.id))
            bes_amount = result_dict.get("individual_pension_net-" + str(contract.id))
            if bes_amount is not None:
                result_dict["amount_net-" + str(contract.id)]['amount'] -= bes_amount['amount']
            else:
                # individual_pension_net değeri bulunamadı, bu durumu işleyin veya hata oluşsun.
                pass  # veya raise ValueError("individual_pension_net value not found for contract: {}".format(contract.id))

            # if ("amount_net-" + str(contract.id)) in result_dict:
            #     result_dict["amount_net-" + str(contract.id)]['amount'] -= result_dict.get("individual_pension_net-" + str(contract.id))[
            #         'amount']

            disabled_amount = 0
            if result_dict.get("disabled_amount_allowance-" + str(contract.id)):
                disabled_amount += result_dict.get("disabled_amount_allowance-" + str(contract.id))['amount']
            if ("after_incentives_income_tax_net-" + str(contract.id)) in result_dict:
                beforeTax = result_dict["after_incentives_income_tax_net-" + str(contract.id)][
                                'amount'] - disabled_amount
            else:
                beforeTax = 0

            disabled = 0
            if contract.disabled_degree == "disabled_1":
                disabled += float(settings_dict['first_degree_disabled_discount'])
            if contract.disabled_degree == "disabled_2":
                disabled += float(settings_dict['second_degree_disabled_discount'])
            if contract.disabled_degree == "disabled_3":
                disabled += float(settings_dict['third_degree_disabled_discount'])
            if disabled > 0 and (result_dict["after_incentives_income_tax_net-" + str(contract.id)]['amount'] > 0):
                result_dict["monthly_tax_base_gross-" + str(contract.id)]['amount'] -= disabled
                result_dict["cumulative_tax_base_gross-" + str(contract.id)]['amount'] -= disabled

                totalTax = result_dict["cumulative_tax_base_gross-" + str(contract.id)]['amount']
                beforeTotal = result_dict["cumulative_tax_base_gross-" + str(contract.id)]['amount'] - \
                              result_dict["monthly_tax_base_gross-" + str(contract.id)]['amount']

                fourthTaxAmount = float(settings_dict['fourth_part_tax'])
                thirdTaxAmount = float(settings_dict['third_part_tax'])
                secondTaxAmount = float(settings_dict['second_part_tax'])
                firstTaxAmount = float(settings_dict['first_part_tax'])

                fifthTaxRatio = float(settings_dict['fifth_part_tax_ratio'])
                fourthTaxRatio = float(settings_dict['fourth_part_tax_ratio'])
                thirdTaxRatio = float(settings_dict['third_part_tax_ratio'])
                secondTaxRatio = float(settings_dict['second_part_tax_ratio'])
                firstTaxRatio = float(settings_dict['first_part_tax_ratio'])

                remainingTax = 0
                if totalTax > fourthTaxAmount:
                    remainingTax += (totalTax - fourthTaxAmount) * fifthTaxRatio + (
                            fourthTaxAmount - thirdTaxAmount) * fourthTaxRatio + (
                                            thirdTaxAmount - secondTaxAmount) * thirdTaxRatio + (
                                            secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif totalTax > thirdTaxAmount:
                    remainingTax += (totalTax - thirdTaxAmount) * fourthTaxRatio + (
                            thirdTaxAmount - secondTaxAmount) * thirdTaxRatio + (
                                            secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif totalTax > secondTaxAmount:
                    remainingTax += (totalTax - secondTaxAmount) * thirdTaxRatio + (
                            secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif totalTax > firstTaxAmount:
                    remainingTax += (totalTax - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                else:
                    remainingTax += totalTax * firstTaxRatio

                remainingTaxBefore = 0

                if beforeTotal > fourthTaxAmount:
                    remainingTaxBefore += (beforeTotal - fourthTaxAmount) * fifthTaxRatio + (
                            fourthTaxAmount - thirdTaxAmount) * fourthTaxRatio + (
                                                  thirdTaxAmount - secondTaxAmount) * thirdTaxRatio + (
                                                  secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif beforeTotal > thirdTaxAmount:
                    remainingTaxBefore += (beforeTotal - thirdTaxAmount) * fourthTaxRatio + (
                            thirdTaxAmount - secondTaxAmount) * thirdTaxRatio + (
                                                  secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif beforeTotal > secondTaxAmount:
                    remainingTaxBefore += (beforeTotal - secondTaxAmount) * thirdTaxRatio + (
                            secondTaxAmount - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                elif beforeTotal > firstTaxAmount:
                    remainingTaxBefore += (
                                                  beforeTotal - firstTaxAmount) * secondTaxRatio + firstTaxAmount * firstTaxRatio

                else:
                    remainingTaxBefore += beforeTotal * firstTaxRatio

                result = max(0, (remainingTax - remainingTaxBefore))
                result_dict["monthly_income_tax_net-" + str(contract.id)]['amount'] = result
                result_dict["after_incentives_income_tax_net-" + str(contract.id)]['amount'] = \
                    result_dict["monthly_income_tax_net-" + str(contract.id)]['amount'] - \
                    result_dict["tax_incentives_deductions-" + str(contract.id)]['amount']
                afterTax = beforeTax - result_dict["after_incentives_income_tax_net-" + str(contract.id)]['amount']
                result_dict["amount_net-" + str(contract.id)]['amount'] += \
                    result_dict.get("disabled_amount_allowance-" + str(contract.id))['amount'] + afterTax

        else:
            for rule in sorted_rules:
                key = rule.code + '-' + str(contract.id)
                local_dict['result'] = None
                local_dict['result_qty'] = 1.0
                local_dict['result_rate'] = 100
                # check if the rule can be applied
                if rule._satisfy_condition(local_dict) and rule.id not in blacklist:
                    # compute the amount of the rule
                    amount, qty, rate = rule._compute_rule(local_dict)
                    # check if there is already a rule computed with that code
                    previous_amount = rule.code in local_dict and local_dict[rule.code] or 0.0
                    # set/overwrite the amount computed for this rule in the local_dict
                    tot_rule = contract.company_id.currency_id.round(amount * qty * rate / 100.0)
                    local_dict[rule.code] = tot_rule
                    rules_dict[rule.code] = rule
                    # sum the amount for its salary category
                    local_dict = _sum_salary_rule_category(local_dict, rule.category_id, tot_rule - previous_amount)
                    # create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_percentage': rule.amount_percentage,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'rate': rate,
                    }

                else:
                    # blacklist this rule and its children
                    blacklist += [id for id, seq in rule._recursive_search_of_rules()]
        # result_dict.pop("gross_earning_gross-" +  str(contract.id))

        return list(result_dict.values())

    def reduce_days_to_30(self):
        total_days = 0
        for worked_days_lines in self.worked_days_line_ids:
            total_days += worked_days_lines.number_of_days
        regular_shift_line = self.worked_days_line_ids.filtered(lambda line: line.code == 'regular_shift_basic')
        if regular_shift_line:
            if total_days - 30 != 0:
                regular_shift_line.number_of_days -= (total_days - 30)
                regular_shift_line.number_of_hours -= (total_days - 30) * 7.5
        sel = self
        _logger.info('************')
        _logger.info(self)

    @api.onchange('employee_id')
    def onchange_contract(self):
        if not self.contract_id:
            self.struct_id = False

        input_lines_1 = self.input_line_ids.browse([])

        for r in initialInputs:
            r['contract_id'] = self.contract_id
            if self.env['hr.payslip.input.type'].search([
                ('name', '=', r['name']),
                ('code', '=', r['code']),
            ]):
                r['input_type_id'] = self.env['hr.payslip.input.type'].search([
                    ('name', '=', r['name']),
                    ('code', '=', r['code']),
                ]).id
            else:
                r['input_type_id'] = self.env['hr.payslip.input.type'].create({
                    'name': r['name'],
                    'code': r['code']
                })
            input_lines_1 += input_lines_1.new(r)
        self.input_line_ids = input_lines_1

        self.with_context(contract=True).onchange_employee()

        approved_leaves = self.env['hr.leave'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'validate'),
            ('request_date_from', '<=', self.date_to),
            ('request_date_to', '>=', self.date_from),
        ])

        paid_leave_days = sum(
            leave.number_of_days for leave in approved_leaves if leave.holiday_status_id.requires_allocation == "yes")
        unpaid_leave_days = sum(
            leave.number_of_days for leave in approved_leaves if leave.holiday_status_id.requires_allocation == "no")

        if not approved_leaves:
            for default_leave in [
                {
                    'name': 'Free vacation',
                    'sequence': 5,
                    'code': 'missing_day_basic',
                    'number_of_days': 0,
                    'number_of_hours': 0,
                    'contract_id': 1,
                }, {
                    'name': 'Paid vacation',
                    'sequence': 4,
                    'code': 'paid_vacation_basic',
                    'number_of_days': 0,
                    'number_of_hours': 0,
                    'contract_id': 1,
                },
            ]:
                if self.env['hr.work.entry.type'].search([
                    ('name', '=', default_leave['name']),
                    ('code', '=', default_leave['code']),
                ]):
                    default_leave['work_entry_type_id'] = self.env['hr.work.entry.type'].search([
                        ('name', '=', default_leave['name']),
                        ('code', '=', default_leave['code']),
                    ]).id
                else:

                    default_leave['work_entry_type_id'] = self.env['hr.work.entry.type'].create({
                        'name': default_leave['name'],
                        'code': default_leave['code']
                    })
        else:
            for default_leave in [
                {
                    'name': 'Free vacation',
                    'sequence': 5,
                    'code': 'missing_day_basic',
                    'number_of_days': unpaid_leave_days,
                    'number_of_hours': unpaid_leave_days * 7.5,
                    'contract_id': 1,
                }, {
                    'name': 'Paid vacation',
                    'sequence': 4,
                    'code': 'paid_vacation_basic',
                    'number_of_days': paid_leave_days,
                    'number_of_hours': paid_leave_days * 7.5,
                    'contract_id': 1,
                },
            ]:
                if self.env['hr.work.entry.type'].search([
                    ('name', '=', default_leave['name']),
                    ('code', '=', default_leave['code']),
                ]):
                    default_leave['work_entry_type_id'] = self.env['hr.work.entry.type'].search([
                        ('name', '=', default_leave['name']),
                        ('code', '=', default_leave['code']),
                    ]).id
                else:

                    default_leave['work_entry_type_id'] = self.env['hr.work.entry.type'].create({
                        'name': default_leave['name'],
                        'code': default_leave['code']
                    })

        regular_shift_line = self.worked_days_line_ids.filtered(lambda line: line.code == 'regular_shift_basic')
        if regular_shift_line:
            regular_shift_line.number_of_days = regular_shift_line.number_of_days - unpaid_leave_days - paid_leave_days
            regular_shift_line.number_of_hours = regular_shift_line.number_of_days * 7.5
        return

    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_id = self.contract_id
            if not contract_id:
                raise ValidationError(
                    _("No running contract found for the employee: %s or no contract in the given period" % payslip.employee_id.name))
            lines = [(0, 0, line) for line in self.get_payslip_lines(payslip.id)]
            payslip.write({'line_ids': lines, 'number': number})
        return True
