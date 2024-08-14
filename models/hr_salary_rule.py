# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.


from odoo import api, fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    condition_python = fields.Text(string='Python Condition', required=True, compute="_compute_condition_python",
                                   store=True)
    amount_python_compute = fields.Text(string='Python Code', compute="_compute_amount_python_compute", store=True)

    input_ids = fields.One2many('hr.payslip.input', 'input_id', string='Inputs', copy=True)
    child_ids = fields.One2many('hr.salary.rule', 'parent_rule_id', string='Child Salary Rule', copy=True)
    parent_rule_id = fields.Many2one('hr.salary.rule', string='Parent Salary Rule', index=True)
    register_id = fields.Many2one('hr.contribution.register', string='Contribution Register',
                                  help="Eventual third party involved in the salary payment of the employees.")

    def _recursive_search_of_rules(self):
        """
        @return: returns a list of tuple (id, sequence) which are all the children of the passed rule_ids
        """
        children_rules = []
        for rule in self.filtered(lambda rule: rule.child_ids):
            children_rules += rule.child_ids._recursive_search_of_rules()
        return [(rule.id, rule.sequence) for rule in self]

    @api.depends('condition_select', 'amount_select', 'active')
    def _compute_condition_python(self):
        for rec in self:
            if rec.condition_select == 'python':
                if rec.code in (
                        'regular_shift_basic', 'weekend_holiday_basic', 'missing_day_basic', 'national_holiday_basic',
                        'extra_shift_basic', 'overtime_shift_basic',
                        'holiday_shift_basic'):
                    rec.condition_python = f"""result = worked_days.{rec.code} and worked_days.{rec.code}.number_of_hours > 0
                            """
                if rec.code == 'total_deductions':
                    rec.condition_python = """result = rules.advance_deductions or rules.execution_deductions or rules.syndicate_deductions or rules.individual_pension_net or rules.missing_day_basic
                            """
                if rec.code == 'food_allowance':
                    rec.condition_python = f"""result = inputs.food_allowance and inputs.food_days_input and inputs.food_allowance.amount > 0
                            """
                if rec.code in (
                        'family_allowance', 'child_allowance', 'bonus_allowance', 'prim_allowance', 'holiday_allowance',
                        'fuel_allowance', 'attendance_allowance', 'death_allowance',
                        'birth_allowance', 'marriage_allowance', 'advance_deductions', 'execution_deductions',
                        'syndicate_deductions', 'severance_allowance', 'notice_allowance', 'road_allowance'):
                    rec.condition_python = f"""result = inputs.{rec.code} and inputs.{rec.code}.amount > 0
                            """
                if rec.code == 'incentives_05510':
                    rec.condition_python = """result = employee.incentive_code == '05510' or ((employee.incentive_code == '06111' or employee.incentive_code == '06645'or employee.incentive_code == '25510' or employee.incentive_code == '16322'or employee.incentive_code == '14857') and employee.benefit_05510)
                            """
                if rec.code == 'incentives_06111':
                    rec.condition_python = """result = (employee.incentive_code == '06111' and (employee.incentive_start_date and employee.incentive_end_date and (payslip.date_from > employee.incentive_start_date and payslip.date_to < employee.incentive_end_date))) or  ((employee.incentive_code == '06645' or employee.incentive_code == '25510' or employee.incentive_code == '16322' or employee.incentive_code == '14857') and employee.benefit_06111)
                            """
                if rec.code == 'incentives_06486':
                    rec.condition_python = """result = employee.incentive_code == '06486'
                            """
                if rec.code == 'incentives_06645':
                    rec.condition_python = """result = employee.incentive_code == '06645' and  not (employee.benefit_05510 or employee.benefit_06111)
                            """
                if rec.code == 'incentives_25510':
                    rec.condition_python = """result = employee.incentive_code == '25510' and  not (employee.benefit_05510 or employee.benefit_06111)
                            """
                if rec.code == 'incentives_16322':
                    rec.condition_python = """result = employee.incentive_code == '16322' and  not (employee.benefit_05510 or employee.benefit_06111)
                            """
                if rec.code == 'incentives_14857':
                    rec.condition_python = """result = employee.incentive_code == '14857' and  not (employee.benefit_06111)
                            """
                if rec.code == 'ssi_employer_share_incentives_deductions':
                    rec.condition_python = """result = False
if rules.incentives_05510 or  rules.incentives_06111 or  rules.incentives_06486 or  rules.incentives_06645 or  rules.incentives_25510 or  rules.incentives_16322 or  rules.incentives_14857:
  result = True
  """
                if rec.code == 'disabled_amount_allowance':
                    rec.condition_python = """result = contract.disabled_degree == 'disabled_1' or contract.disabled_degree == 'disabled_2' or contract.disabled_degree == 'disabled_3'
                            """
                if rec.code == 'amount_net':
                    rec.condition_python = """result = rules.GROSS > categories.GROSS"""
            else:
                rec.condition_python = "TRUE"

    @api.depends('condition_select', 'amount_select', 'active')
    def _compute_amount_python_compute(self):
        for rec in self:
            if rec.amount_select == 'code':
                if rec.code in ('regular_shift_basic', 'weekend_holiday_basic', 'missing_day_basic'):
                    rec.amount_python_compute = f"""a_HourValue = contract.wage/225

if worked_days.{rec.code}:
    result = worked_days.{rec.code}.number_of_hours*a_HourValue
else:
    result = 0
"""
                if rec.code == 'total_deductions':
                    rec.amount_python_compute = """a_HourValue = contract.wage/225
negativeValue = 0
if rules.missing_day_basic:
  negativeValue +=missing_day_basic

if rules.advance_deductions:
  negativeValue += advance_deductions
if rules.execution_deductions:
  negativeValue += execution_deductions
if rules.syndicate_deductions:
  negativeValue += syndicate_deductions
if rules.individual_pension_net:
  negativeValue += individual_pension_net
result = negativeValue
"""
                if rec.code in ('national_holiday_basic', 'extra_shift_basic', 'overtime_shift_basic', 'holiday_shift'):
                    rec.amount_python_compute = f"""a_HourValue = contract.wage/225
if worked_days.{rec.code}:
  result = worked_days.{rec.code}.number_of_hours*a_HourValue*float(settings.extra_shift_rate)
else:
  result = 0
"""
                if rec.code in (
                        'food_allowance', 'family_allowance', 'child_allowance', 'bonus_allowance', 'prim_allowance',
                        'holiday_allowance', 'fuel_allowance', 'attendance_allowance', 'death_allowance',
                        'birth_allowance',
                        'marriage_allowance', 'advance_deductions', 'execution_deductions', 'syndicate_deductions',
                        'severance_allowance', 'notice_allowance', 'road_allowance'):
                    rec.amount_python_compute = f"""result = inputs.{rec.code}.amount
                            """
                if rec.code == 'amount_gross':
                    rec.amount_python_compute = """a_HourValue = contract.wage/225
mainValue = 0
if worked_days.regular_shift_basic:
  mainValue += worked_days.regular_shift_basic.number_of_hours * a_HourValue
if worked_days.weekend_holiday_basic:
  mainValue += worked_days.weekend_holiday_basic.number_of_hours * a_HourValue
if worked_days.national_holiday_basic:
  mainValue += worked_days.national_holiday_basic.number_of_hours * a_HourValue
if worked_days.paid_vacation_basic:
  mainValue += worked_days.paid_vacation_basic.number_of_hours * a_HourValue

negativeValue = 0
if worked_days.missing_day_basic:
  negativeValue += worked_days.missing_day_basic.number_of_hours * a_HourValue
result = max((mainValue - negativeValue),0)
"""
                if rec.code == 'gross_earning_gross':
                    rec.amount_python_compute = """others = 0
minimum_wage = settings.gross_minimum_wage
if inputs.bonus_allowance:
  others += inputs.bonus_allowance.amount
if inputs.prim_allowance:
  others += inputs.prim_allowance.amount
if inputs.birth_allowance:
    others += inputs.birth_allowance.amount
if inputs.death_allowance:
  others += inputs.death_allowance.amount
if inputs.marriage_allowance:
  others += inputs.marriage_allowance.amount
if inputs.attendance_allowance:
  others += inputs.attendance_allowance.amount
if inputs.holiday_allowance:
  others += inputs.holiday_allowance.amount
if inputs.fuel_allowance:
  others += inputs.fuel_allowance.amount
if rules.food_allowance:
  others +=food_allowance
if rules.road_allowance:
  others +=road_allowance
if rules.child_allowance:
  others +=child_allowance
if rules.family_allowance:
  others += family_allowance
if rules.severance_allowance:
  others += severance_allowance
if rules.notice_allowance:
  others += notice_allowance

if rules.extra_shift_basic:
  others += extra_shift_basic
if rules.overtime_shift_basic:
  others += overtime_shift_basic
if rules.holiday_shift_basic:
  others += holiday_shift_basic
result = max((amount_gross + others),0)
"""
                if rec.code == 'ssi_base_gross':
                    rec.amount_python_compute = """others = 0
minimum_wage = settings.gross_minimum_wage
daily_minimum_wage = 0
if inputs.food_days_input:
  daily_minimum_wage = (float(minimum_wage)/30)*inputs.food_days_input.amount*float(settings.food_allowance_rate)
family_minimum_wage = float(minimum_wage)*float(settings.family_allowance_rate)
if inputs.bonus_allowance:
  others += inputs.bonus_allowance.amount
if inputs.prim_allowance:
  others += inputs.prim_allowance.amount
if inputs.holiday_allowance:
  others += inputs.holiday_allowance.amount
if inputs.fuel_allowance:
  others += inputs.fuel_allowance.amount
if rules.road_allowance:
  others +=road_allowance
if rules.child_allowance:
  others +=child_allowance
if rules.family_allowance:
  others +=max(0,family_allowance-family_minimum_wage)
if rules.food_allowance:
  others +=food_allowance              
if rules.extra_shift_basic:
  others += extra_shift_basic
if rules.overtime_shift_basic:
  others += overtime_shift_basic
if rules.holiday_shift_basic:
  others += holiday_shift_basic

result = max((min((amount_gross+others),float(settings.ssi_ceiling_amount))),0)
"""
                if rec.code == 'ssi_worker_prim_rate_deductions':
                    rec.amount_python_compute = """ratio = settings.ssi_worker_prim_rate

if contract.contract_type_id.name == 'Retired':
  ratio = settings.ssi_worker_retired_rate
result = (ssi_base_gross * float(ratio))
"""
                if rec.code == 'ssi_unemployment_worker_prim_rate_deductions':
                    rec.amount_python_compute = """if contract.contract_type_id.name == 'Retired':
  result = 0
else:
  result = (ssi_base_gross * float(settings.ssi_unemployment_worker_rate))
"""
                if rec.code == 'ssi_employer_prim_rate_basic':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if contract.contract_type_id.name == 'Retired':
  ratio = float(settings.ssi_employer_retired_rate)

result = ssi_base_gross * float(ratio)
"""
                if rec.code == 'ssi_unemployment_employer_prim_rate_gross':
                    rec.amount_python_compute = """if contract.contract_type_id.name == 'Retired':
  result = 0
else:
  result = ssi_base_gross * float(settings.ssi_unemployment_employer_rate)
"""
                if rec.code == 'incentives_05510':
                    rec.amount_python_compute = """result = ssi_base_gross * float(0.05)
                            """
                if rec.code == 'incentives_06111':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if employee.benefit_05510:
  ratio -= 0.05
result = ssi_base_gross * float(ratio)
"""
                if rec.code == 'incentives_06486':
                    rec.amount_python_compute = """result = float(settings.gross_minimum_wage) * float(0.05)"""
                if rec.code == 'incentives_06645':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if employee.benefit_05510:
  ratio -= 0.05
if employee.benefit_06111:
  ratio = 0

if ratio == float(settings.ssi_employer_prim_rate):
   ratio -= 0.05
result = float(settings.gross_minimum_wage) * float(ratio)
"""
                if rec.code == 'incentives_25510':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if employee.benefit_05510:
  ratio -= 0.05
if employee.benefit_06111:
  ratio = 0

if ratio == float(settings.ssi_employer_prim_rate):
   ratio -= 0.05
result = float(settings.gross_minimum_wage) * float(ratio)
"""
                if rec.code == 'incentives_16322':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if employee.benefit_05510:
  ratio -= 0.05
if employee.benefit_06111:
  ratio = 0
result = float(settings.gross_minimum_wage) * float(ratio)
"""
                if rec.code == 'incentives_14857':
                    rec.amount_python_compute = """ratio = float(settings.ssi_employer_prim_rate)
if employee.benefit_05510:
  ratio -= 0.05
if employee.benefit_06111:
  ratio = 0
result = float(settings.gross_minimum_wage) * float(ratio)
"""
                if rec.code == 'stamp_tax_base_basic':
                    rec.amount_python_compute = """others = 0
if rules.severance_allowance:
  others += severance_allowance
if rules.notice_allowance:
  others += notice_allowance
if rules.attendance_allowance:
  others += attendance_allowance
if rules.birth_allowance:
  others += birth_allowance
if(ssi_base_gross >=float(settings.ssi_ceiling_amount)):
  result = gross_earning_gross
else:
  result = ssi_base_gross + others
"""
                if rec.code == 'stamp_tax_incentives_deductions':
                    rec.amount_python_compute = """result = float(settings.gross_minimum_wage)"""
                if rec.code == 'after_incentives_stamp_tax_base_net':
                    rec.amount_python_compute = """result = max(0,stamp_tax_base_basic-stamp_tax_incentives_deductions)"""
                if rec.code == 'ssi_employer_share_incentives_deductions':
                    rec.amount_python_compute = """result = 0

if rules.incentives_05510:
  result += incentives_05510

if rules.incentives_06111:
  result += 	incentives_06111

if rules.incentives_06486:
  result += 	incentives_06486
if rules.incentives_06645:
  result += 	incentives_06645

if rules.incentives_25510:
  result += 	incentives_25510

if rules.incentives_16322:
  result += 	incentives_16322

if rules.incentives_14857:
  result += 	incentives_14857
"""
                if rec.code == 'stamp_tax_deductions':
                    rec.amount_python_compute = """result = after_incentives_stamp_tax_base_net*float(settings.stump_tax_rate)"""
                if rec.code == 'monthly_tax_base_gross':
                    rec.amount_python_compute = """discount = 0
if rules.syndicate_deductions:
  discount += syndicate_deductions          
others = 0             
if rules.notice_allowance:
  others += notice_allowance
if rules.attendance_allowance:
  others += attendance_allowance
doubleBrut = 2 * amount_gross
if rules.marriage_allowance and marriage_allowance > doubleBrut:
  others += marriage_allowance - doubleBrut
if rules.birth_allowance and birth_allowance > doubleBrut:
  others += birth_allowance - doubleBrut          
if(ssi_base_gross >=float(settings.ssi_ceiling_amount)):
  result = max(0,gross_earning_gross-ssi_worker_prim_rate_deductions-ssi_unemployment_worker_prim_rate_deductions-discount)
else:
  result = max(0,ssi_base_gross-ssi_worker_prim_rate_deductions-ssi_unemployment_worker_prim_rate_deductions-discount + others)                      
"""
                if rec.code == 'monthly_minimum_wage_tax_base_gross':
                    rec.amount_python_compute = """minimum_wage = float(settings.gross_minimum_wage)
unemployment_worker_rate = float(settings.ssi_unemployment_worker_rate)
ssi = float(settings.ssi_worker_prim_rate)
result = minimum_wage-(minimum_wage*(unemployment_worker_rate+ssi))
"""
                if rec.code == 'individual_pension_net':
                    rec.amount_python_compute = """result = gross_earning_gross * float(settings.individual_pension_rate)
result = 0
"""
                if rec.code == 'cumulative_tax_base_gross':
                    rec.amount_python_compute = """year = str(payslip.date_from.year)
end_date = str(payslip.date_from)
before = 0
if contract.previous_cumulative_tax_base:
  before += contract.previous_cumulative_tax_base

result = payslip.sum('monthly_tax_base_gross','01/01/'+year,end_date) + monthly_tax_base_gross + before
"""
                if rec.code == 'cumulative_minimum_wage_tax_base_gross':
                    rec.amount_python_compute = """year = str(payslip.date_from.year)
end_date = str(payslip.date_from)
result = payslip.sum('monthly_minimum_wage_tax_base_gross','01/01/'+year,end_date) + monthly_minimum_wage_tax_base_gross
"""
                if rec.code == 'tax_incentives_deductions':
                    rec.amount_python_compute = """totalTax = cumulative_minimum_wage_tax_base_gross
beforeTotal = cumulative_minimum_wage_tax_base_gross - monthly_minimum_wage_tax_base_gross
fourthTaxAmount = float(settings.fourth_part_tax)
thirdTaxAmount = float(settings.third_part_tax)
secondTaxAmount = float(settings.second_part_tax)
firstTaxAmount = float(settings.first_part_tax)

fifthTaxRatio = float(settings.fifth_part_tax_ratio)
fourthTaxRatio = float(settings.fourth_part_tax_ratio)
thirdTaxRatio = float(settings.third_part_tax_ratio)
secondTaxRatio = float(settings.second_part_tax_ratio)
firstTaxRatio = float(settings.first_part_tax_ratio)
remainingTax = 0
if totalTax > fourthTaxAmount:
  remainingTax += (totalTax-fourthTaxAmount)*fifthTaxRatio + fourthTaxRatio*fourthTaxAmount
elif totalTax > thirdTaxAmount:
  remainingTax += (totalTax-thirdTaxAmount)*fourthTaxRatio + thirdTaxRatio*thirdTaxAmount
elif totalTax > secondTaxAmount:
  remainingTax += (totalTax-secondTaxAmount)*thirdTaxRatio + secondTaxRatio*secondTaxAmount
elif totalTax > firstTaxAmount:
  remainingTax += (totalTax-firstTaxAmount)*secondTaxRatio + firstTaxRatio*firstTaxAmount
else:
  remainingTax += totalTax*firstTaxRatio

remainingTaxBefore = 0
if beforeTotal > fourthTaxAmount:
  remainingTaxBefore += (beforeTotal-fourthTaxAmount)*fifthTaxRatio + fourthTaxRatio*fourthTaxAmount
elif beforeTotal > thirdTaxAmount:
  remainingTaxBefore += (beforeTotal-thirdTaxAmount)*fourthTaxRatio + thirdTaxRatio*thirdTaxAmount
elif beforeTotal > secondTaxAmount:
  remainingTaxBefore += (beforeTotal-secondTaxAmount)*thirdTaxRatio + secondTaxRatio*secondTaxAmount
elif beforeTotal > firstTaxAmount:
  remainingTaxBefore += (beforeTotal-firstTaxAmount)*secondTaxRatio + firstTaxRatio*firstTaxAmount
else:
  remainingTaxBefore += beforeTotal*firstTaxRatio

result = remainingTax - remainingTaxBefore
"""
                if rec.code == 'monthly_income_tax_net':
                    rec.amount_python_compute = """totalTax = 	cumulative_tax_base_gross
beforeTotal = 	cumulative_tax_base_gross - monthly_tax_base_gross
amount = 0
if contract.disabled_degree == 'disabled_1':
  amount = float(settings.first_degree_disabled_discount)
if contract.disabled_degree == 'disabled_2':
  amount = float(settings.second_degree_disabled_discount)
if contract.disabled_degree == 'disabled_3':
  amount = float(settings.third_degree_disabled_discount)
#totalTax -= amount

fourthTaxAmount = float(settings.fourth_part_tax)
thirdTaxAmount = float(settings.third_part_tax)
secondTaxAmount = float(settings.second_part_tax)
firstTaxAmount = float(settings.first_part_tax)

fifthTaxRatio = float(settings.fifth_part_tax_ratio)
fourthTaxRatio = float(settings.fourth_part_tax_ratio)
thirdTaxRatio = float(settings.third_part_tax_ratio)
secondTaxRatio = float(settings.second_part_tax_ratio)
firstTaxRatio = float(settings.first_part_tax_ratio)
remainingTax = 0
if totalTax > fourthTaxAmount:
  remainingTax += (totalTax-fourthTaxAmount)*fifthTaxRatio + (fourthTaxAmount-thirdTaxAmount)*fourthTaxRatio + (thirdTaxAmount-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio          
elif totalTax > thirdTaxAmount:
  remainingTax += (totalTax-thirdTaxAmount)*fourthTaxRatio + (thirdTaxAmount-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio           
elif totalTax > secondTaxAmount:
  remainingTax += (totalTax-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio          
elif totalTax > firstTaxAmount:
  remainingTax += (totalTax-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio           
else:
  remainingTax += totalTax*firstTaxRatio                        
remainingTaxBefore = 0      
if beforeTotal > fourthTaxAmount:
  remainingTaxBefore += (beforeTotal-fourthTaxAmount)*fifthTaxRatio + (fourthTaxAmount-thirdTaxAmount)*fourthTaxRatio + (thirdTaxAmount-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio        
elif beforeTotal > thirdTaxAmount:
  remainingTaxBefore += (beforeTotal-thirdTaxAmount)*fourthTaxRatio + (thirdTaxAmount-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio                        
elif beforeTotal > secondTaxAmount:
  remainingTaxBefore += (beforeTotal-secondTaxAmount)*thirdTaxRatio + (secondTaxAmount-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio           
elif beforeTotal > firstTaxAmount:
  remainingTaxBefore += (beforeTotal-firstTaxAmount)*secondTaxRatio + firstTaxAmount*firstTaxRatio            
else:
  remainingTaxBefore += beforeTotal*firstTaxRatio

result = max(0,(remainingTax - remainingTaxBefore))
"""
                if rec.code == 'disabled_amount_allowance':
                    rec.amount_python_compute = """totalTax = 	cumulative_tax_base_gross
beforeTotal = 	cumulative_tax_base_gross - monthly_tax_base_gross
amount = 0
if contract.disabled_degree == 'disabled_1':
  amount = float(settings.first_degree_disabled_discount)
if contract.disabled_degree == 'disabled_2':
  amount = float(settings.second_degree_disabled_discount)
if contract.disabled_degree == 'disabled_3':
  amount = float(settings.third_degree_disabled_discount)
totalTax -=amount
fourthTaxAmount = float(settings.fourth_part_tax)
thirdTaxAmount = float(settings.third_part_tax)
secondTaxAmount = float(settings.second_part_tax)
firstTaxAmount = float(settings.first_part_tax)

fifthTaxRatio = float(settings.fifth_part_tax_ratio)
fourthTaxRatio = float(settings.fourth_part_tax_ratio)
thirdTaxRatio = float(settings.third_part_tax_ratio)
secondTaxRatio = float(settings.second_part_tax_ratio)
firstTaxRatio = float(settings.first_part_tax_ratio)
restrictedAmount = 0
if totalTax > fourthTaxAmount:
  restrictedAmount += amount*fifthTaxRatio
elif totalTax > thirdTaxAmount:
  restrictedAmount += amount*fourthTaxAmount
elif totalTax > secondTaxAmount:
  restrictedAmount += amount*thirdTaxRatio

elif totalTax > firstTaxAmount:
  restrictedAmount += amount*secondTaxRatio
else:
  restrictedAmount += amount*firstTaxRatio

result = restrictedAmount
"""
                if rec.code == 'after_incentives_income_tax_net':
                    rec.amount_python_compute = """result = 	max(0,(monthly_income_tax_net -	tax_incentives_deductions))"""
                if rec.code == 'amount_net':
                    rec.amount_python_compute = """others = 0
if rules.advance_deductions:
    others += advance_deductions
if rules.execution_deductions:
    others += execution_deductions
if rules.syndicate_deductions:
    others += syndicate_deductions

if rules.individual_pension_net and contract.type_salary == 'gross':
    others += individual_pension_net

result = gross_earning_gross-(ssi_worker_prim_rate_deductions + ssi_unemployment_worker_prim_rate_deductions +	stamp_tax_deductions +	after_incentives_income_tax_net) - others
"""
                # if rec.code == 'Travel':
                #     rec.amount_python_compute = """result = contract.travel_allowance"""
            else:
                rec.amount_python_compute = "TRUE"
