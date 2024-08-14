# Copyright 2024 Akkurt Volkan
# License AGPL-3.0.


from odoo import api, fields, models


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    def get_all_rules(self):
        """
        @return: returns a list of tuple (id, sequence) of rules that are maybe to apply
        """
        all_rules = []
        for struct in self:
            all_rules += struct.rule_ids._recursive_search_of_rules()
        return all_rules

    def _get_parent_structure(self):
        parent_ids = []
        parent = self.mapped('parent_id')
        if parent:
            parent_ids = parent._get_parent_structure()
        parent_ids.append(self.id)
        return parent_ids

    @api.model
    def _get_parent(self):
        return self.env.ref('l10n_tr_hr_payroll.l10n_tr_standard_payroll', False)

    parent_id = fields.Many2one('hr.payroll.structure', string='Parent', default=_get_parent)

