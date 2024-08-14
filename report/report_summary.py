# -*- coding:utf-8 -*-

from odoo import api, models
from odoo.exceptions import MissingError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrEmployeeSummaryReport(models.AbstractModel):
    _name = 'report.l10n_tr_hr_payroll.report_summary_templates'
    _description = 'Summary Report'

    def get_calculate(self, employee_ids, date_from):
        # sgk ile alakali degiskenler
        ssi_worker = 0
        ssi_employer = 0
        ssi_unemployment_worker_rate = 0
        ssi_unemployment_employer_rate = 0
        ssi_total = 0
        ssi_unemployment_total = 0
        gross_amount_total = 0
        net_amount_total = 0
        individual_pension = 0
        income_tax_base = 0
        income_tax_first = 0
        income_tax_incentives = 0
        income_tax_last = 0
        stamp_tax_base = 0
        stamp_tax_first = 0
        stamp_tax_incentives = 0
        stamp_tax_last = 0
        worker_deductions_total = 0
        employer_deductions_total = 0

        # gelirler raporu ile alakali degiskenler
        road_allowance = 0
        bonus_allowance = 0
        notice_allowance = 0
        severance_allowance = 0
        prim_allowance = 0
        syndicate_deductions = 0
        execution_deductions = 0
        advance_deductions = 0
        other = 0
        total_deductions = 0
        net_other_incomes_total = 0
        net_incomes_total = 0
        gross_incomes_total = 0
        net_profit = 0

        # mesailer ile alakali degiskenler
        extra_shift = 0
        extra_shift_amount = 0
        overtime_shift = 0
        overtime_shift_amount = 0
        holiday_shift = 0
        holiday_shift_amount = 0
        total_shift = 0
        total_shift_amount = 0
        missing_days = 0
        missing_days_amount = 0
        regular_shift = 0
        holiday_days = 0
        vacation_days = 0

        month = False
        lines = False
        input_lines = False
        worked_days_lines = False

        employee_total = 0
        employees = self.env['hr.employee'].browse(employee_ids)
        for employee in employees:
            employee_total += 1
            contract_wage = employee.contract_id.wage
            counter = 0
            for employee_slip in employee.slip_ids:
                if str(employee_slip.date_from) == str(date_from):
                    counter = counter + 1
                    month = str(employee_slip.date_from.strftime("%B")) + ' Summary Report'
                    lines = employee_slip.line_ids
                    input_lines = employee_slip.input_line_ids
                    worked_days_lines = employee_slip.worked_days_line_ids
            if counter == 0:
                message = 'Incorrect Date Entered!'
                raise ValidationError(message)
            for line in lines:
                if line.code == 'ssi_worker_prim_rate_deductions':
                    ssi_worker += line.total
                if line.code == 'ssi_employer_prim_rate_deductions':
                    ssi_employer += line.total
                if line.code == 'ssi_unemployment_worker_prim_rate_deductions':
                    ssi_unemployment_worker_rate += line.total
                if line.code == 'ssi_unemployment_employer_prim_rate_gross':
                    ssi_unemployment_employer_rate += line.total
                if line.code == 'gross_earning_gross':
                    gross_amount_total += line.total
                if line.code == 'amount_net':
                    net_amount_total += line.total
                if line.code == 'individual_pension_net':
                    individual_pension += line.total
                if line.code == 'monthly_tax_base_gross':
                    income_tax_base += line.total
                if line.code == 'monthly_income_tax_net':
                    income_tax_first += line.total
                if line.code == 'tax_incentives_deductions':
                    income_tax_incentives += line.total
                if line.code == 'after_incentives_income_tax_net':
                    income_tax_last += line.total
                if line.code == 'stamp_tax_base_basic':
                    stamp_tax_base += line.total
                if line.code == 'stamp_tax_deductions':
                    stamp_tax_first += line.total
                if line.code == 'stamp_tax_incentives_deductions':
                    stamp_tax_incentives += line.total
                if line.code == 'after_incentives_stamp_tax_base_net':
                    stamp_tax_last += line.total
            worker_deductions_total = ssi_worker + ssi_unemployment_worker_rate + income_tax_last + stamp_tax_last
            employer_deductions_total = ssi_employer + ssi_unemployment_employer_rate
            ssi_total = ssi_worker + ssi_employer
            ssi_unemployment_total = ssi_unemployment_worker_rate + ssi_unemployment_employer_rate
            for line in input_lines:
                if line.code == 'road_allowance':
                    road_allowance += line.amount
                elif line.code == 'bonus_allowance':
                    bonus_allowance += line.amount
                elif line.code == 'notice_allowance':
                    notice_allowance += line.amount
                elif line.code == 'severance_allowance':
                    severance_allowance += line.amount
                elif line.code == 'prim_allowance':
                    prim_allowance += line.amount
                elif line.code == 'syndicate_deductions':
                    syndicate_deductions += line.amount
                elif line.code == 'execution_deductions':
                    execution_deductions += line.amount
                elif line.code == 'advance_deductions':
                    advance_deductions += line.amount
                else:
                    other += line.amount  # TODO: Burada eklenen herhangi bir line gelir olarak gözükecek
            for line in worked_days_lines:  # TODO: Burada katsayıları ile eklenecek
                if line.code == 'extra_shift_basic':
                    extra_shift += line.number_of_hours
                    extra_shift_amount = extra_shift * contract_wage / 225
                if line.code == 'overtime_shift_basic':
                    overtime_shift += line.number_of_hours
                    overtime_shift_amount = overtime_shift * contract_wage / 225
                if line.code == 'holiday_shift_basic':
                    holiday_shift += line.number_of_hours
                    holiday_shift_amount = holiday_shift * contract_wage / 225
                if line.code == 'regular_shift_basic':
                    regular_shift += line.number_of_days
                if line.code in ('weekend_holiday_basic', 'national_holiday_basic'):
                    holiday_days += line.number_of_days
                if line.code == 'paid_vacation_basic':
                    vacation_days += line.number_of_days
                if line.code == 'missing_day_basic':
                    missing_days += line.number_of_days
            if missing_days != 0:
                missing_days_amount = contract_wage / 30 * missing_days
            else:
                missing_days_amount = 0
            total_deductions = advance_deductions + execution_deductions + syndicate_deductions + individual_pension + missing_days_amount
            total_shift = extra_shift + overtime_shift + holiday_shift
            total_shift_amount = extra_shift_amount + overtime_shift_amount + holiday_shift_amount
            net_other_incomes_total = road_allowance + bonus_allowance + notice_allowance + severance_allowance + prim_allowance + other
            gross_incomes_total = gross_amount_total  # TODO: Buraya brüt diğer gelirler eklenecek
            net_incomes_total = net_amount_total + net_other_incomes_total
            net_profit = net_incomes_total - total_deductions
            # isci_maliyeti = gross_incomes_total + employer_deductions_total -  # TODO: Burası hesaplanacak sonrasında
        data = {
            'month': month,
            'employee_total': employee_total,
            'ssi_worker': "{:.2f}".format(ssi_worker),
            'ssi_employer': "{:.2f}".format(ssi_employer),
            'ssi_unemployment_worker_rate': "{:.2f}".format(ssi_unemployment_worker_rate),
            'ssi_unemployment_employer_rate': "{:.2f}".format(ssi_unemployment_employer_rate),
            'gross_amount_total': "{:.2f}".format(gross_amount_total),
            'net_amount_total': "{:.2f}".format(net_amount_total),
            'ssi_total': "{:.2f}".format(ssi_total),
            'ssi_unemployment_total': "{:.2f}".format(ssi_unemployment_total),
            'individual_pension': "{:.2f}".format(individual_pension),
            'income_tax_base': "{:.2f}".format(income_tax_base),
            'income_tax_first': "{:.2f}".format(income_tax_first),
            'income_tax_incentives': "{:.2f}".format(income_tax_incentives),
            'income_tax_last': "{:.2f}".format(income_tax_last),
            'stamp_tax_base': "{:.2f}".format(stamp_tax_base),
            'stamp_tax_first': "{:.2f}".format(stamp_tax_first),
            'stamp_tax_incentives': "{:.2f}".format(stamp_tax_incentives),
            'stamp_tax_last': "{:.2f}".format(stamp_tax_last),
            'worker_deductions_total': "{:.2f}".format(worker_deductions_total),
            'employer_deductions_total': "{:.2f}".format(employer_deductions_total),
            'net_other_incomes_total': "{:.2f}".format(net_other_incomes_total),
            'gross_incomes_total': "{:.2f}".format(gross_incomes_total),
            'net_incomes_total': "{:.2f}".format(net_incomes_total),
            'net_profit': "{:.2f}".format(net_profit),

            'road_allowance': "{:.2f}".format(road_allowance),
            'bonus_allowance': "{:.2f}".format(bonus_allowance),
            'notice_allowance': "{:.2f}".format(notice_allowance),
            'severance_allowance': "{:.2f}".format(severance_allowance),
            'prim_allowance': "{:.2f}".format(prim_allowance),
            'syndicate_deductions': "{:.2f}".format(syndicate_deductions),
            'execution_deductions': "{:.2f}".format(execution_deductions),
            'advance_deductions': "{:.2f}".format(advance_deductions),
            'other': "{:.2f}".format(other),
            'total_deductions': "{:.2f}".format(total_deductions),

            'extra_shift': "{:.2f}".format(extra_shift),
            'extra_shift_amount': "{:.2f}".format(extra_shift_amount),
            'overtime_shift': "{:.2f}".format(overtime_shift),
            'overtime_shift_amount': "{:.2f}".format(overtime_shift_amount),
            'holiday_shift': "{:.2f}".format(holiday_shift),
            'holiday_shift_amount': "{:.2f}".format(holiday_shift_amount),
            'total_shift': "{:.2f}".format(total_shift),
            'total_shift_amount': "{:.2f}".format(total_shift_amount),
            'regular_shift': "{:.2f}".format(regular_shift),
            'holiday_days': "{:.2f}".format(holiday_days),
            'vacation_days': "{:.2f}".format(vacation_days),
            'missing_days': "{:.2f}".format(missing_days),
            'missing_days_amount': "{:.2f}".format(missing_days_amount),
        }
        return data

    def get_incentives(self, employee_ids, date_from):
        employees = self.env['hr.employee'].browse(employee_ids)
        incentives_list = []
        total = 0

        lines = False
        for employee in employees:
            for employee_slip in employee.slip_ids:
                if str(employee_slip.date_from) == str(date_from):
                    lines = employee_slip.line_ids
            for line in lines:
                if line['category_id']['code'] == 'incentives':
                    name = line['name']
                    incentive_total = "{:.2f}".format(line['total'])
                    found = False
                    for item in incentives_list:
                        if item['name'] == name:
                            item['incentive_total'] = "{:.2f}".format(
                                float(item['incentive_total']) + float(incentive_total))
                            found = True
                            break
                    if not found:
                        incentives_list.append({'name': name, 'incentive_total': incentive_total})
                    total += float(incentive_total)
        data = {
            'incentives_list': incentives_list,
            'total': "{:.2f}".format(total),
        }
        return data

    @api.model
    def _get_report_values(self, docids, data=None):

        model = 'hr.employee'
        data = data
        employee_ids = data['form']['employee_ids']
        date_from = data['form']['date_from']
        employees = self.env['hr.employee'].browse(employee_ids)
        missing_employee = []
        message = 'The following employees are missing payroll information:\n'
        for employee in employees:
            if not employee.slip_ids:
                message += '- {}\n'.format(employee.name)
                missing_employee += employee
        message += 'Remove the employee and try again.'
        if missing_employee:
            raise MissingError(message)
        else:
            return {
                'doc_ids': docids,
                'doc_model': model,
                'data': data,
                'docs': employees,
                'get_calculate': self.get_calculate(employee_ids, date_from),
                'incentives': self.get_incentives(employee_ids, date_from)
            }
