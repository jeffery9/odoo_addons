# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import api, fields, models
from odoo.tools.translate import _


class CostActivity(models.Model):
    _name = 'account.cost.activity'
    _description = 'Cost Pool'

    name = fields.Char(string='Name', required=True)
    measure = fields.Char(string=u'Measure Unit', required=True)
    value = fields.Boolean(string=u'Measure this?', default=True)

    driver_id = fields.Many2one(
        string=u'Driver',
        comodel_name='account.cost.driver',
        ondelete='restrict',
        deprecated=True
    )


class CostDriver(models.Model):
    _name = 'account.cost.driver'
    _description = 'Cost Driver'

    name = fields.Char(string='Name')
    driver_type = fields.Selection(
        string='Driver Type',
        selection=[
            ('activity', 'Activity Driver'),
            ('resource', 'Resource Driver'),
        ],
        default='activity'
    )

    activity_id = fields.One2many(
        comodel_name='account.cost.activity',
        inverse_name='driver_id',
        string='Cost Activity'
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_activity_ids = fields.Many2many(
        string=u'Cost Pool',
        comodel_name='account.cost.activity',
        relation='account_cost_activity_product_tmpl_rel',
        column1='account_cost_activity_id',
        column2='product_tmpl_id',
    )


class CostingPlan(models.Model):
    _name = 'account.costing.abc.plan'
    _description = 'Costing Plan'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'name'
    _order = 'name ASC'

    object_type = fields.Selection(
        string=u'Object Type',
        selection=[('product', 'Product'), ('partner', 'Partner')],
        default='product'
    )

    name = fields.Char(
        string=u'Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    date_begin = fields.Date(
        string=u'Date Begin',
        default=fields.Date.context_today,
    )

    date_end = fields.Date(
        string=u'Date End',
        default=fields.Date.context_today,
    )

    product_ids = fields.Many2many(
        string=u'Product',
        comodel_name='product.product',
        relation='product_product_costing_plan_rel',
        column1='product_product_id',
        column2='costing_plan_id',
        required=True
    )

    partner_ids = fields.Many2many(
        string=u'Partner',
        comodel_name='res.partner',
        relation='res_partner_costing_plan_rel',
        column1='res_partner_id',
        column2='costing_plan_id',
    )

    account_ids = fields.Many2many(
        string=u'Account',
        comodel_name='account.account',
        relation='account_account_costing_plan_rel',
        column1='account_account_id',
        column2='costing_plan_id',
        required=True,
        domain=[('internal_group', '=', 'expense')]
    )

    account_move_ids = fields.Many2many(
        string=u'Account Move',
        comodel_name='account.move',
        relation='account_move_costing_plan_rel',
        column1='account_move_id',
        column2='costing_plan_id',
    )

    amount_debit = fields.Float(string=u'Amount Debit', )

    amount_credit = fields.Float(string=u'Amount Credit', )

    amount = fields.Float(string=u'Amount', )

    cost_activity_ids = fields.Many2many(
        string=u'Cost Pool',
        comodel_name='account.cost.activity',
        relation='account_cost_activity_costing_plan_rel',
        column1='account_cost_activity_id',
        column2='costing_plan_id',
    )

    activity_distribution_ids = fields.One2many(
        string=u'Activity Distribution',
        comodel_name='account.costing.abc.plan.activity.distribution',
        inverse_name='plan_id',
    )

    result_ids = fields.One2many(
        string=u'Result',
        comodel_name='account.cost.result',
        inverse_name='plan_id',
    )

    state = fields.Selection(
        string=u'State',
        selection=[
            ('draft', 'Draft'), ('confirmed', 'Confirmed'),
            ('closed', 'Closed'), ('cancelled', 'Cancelled')
        ],
        default='draft',
        readonly=True,
    )

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        for record in self:
            cost_pool_ids = record.product_ids.cost_activity_ids
            exists_cost_pool_ids = record.activity_distribution_ids.mapped(
                'activity_id'
            )
            need_update = cost_pool_ids - exists_cost_pool_ids

            record.cost_activity_ids = cost_pool_ids
            values = []
            for item in need_update:
                values.append((0, 0, {'activity_id': item.id, 'percent': 0}))

            if values:
                record.write({'activity_distribution_ids': values})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_close(self):
        self.write({'state': 'closed'})


class CostingPlanActivityDistribution(models.Model):
    _name = 'account.costing.abc.plan.activity.distribution'
    _description = 'Costing Plan Activity Distribution'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string=u'Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    plan_id = fields.Many2one(
        string=u'Plan',
        comodel_name='account.costing.abc.plan',
        ondelete='restrict',
    )

    product_ids = fields.Many2many(
        string=u'Product',
        comodel_name='product.product',
        relation='product_product_activity_dist_rel',
        column1='product_product_id',
        column2='activity_dist_id',
        compute='_compute_product_ids'
    )

    @api.depends('plan_id')
    def _compute_product_ids(self):
        for record in self:
            record.product_ids = record.plan_id.product_ids.ids

    activity_id = fields.Many2one(
        string=u'Cost Activity',
        comodel_name='account.cost.activity',
        ondelete='restrict',
    )

    measure = fields.Char(
        string=u'Measure',
        related='activity_id.measure',
    )

    percent = fields.Float(string=u'Percent', required=True)

    cost = fields.Float(string=u'Cost', compute='_compute_rate')

    activity = fields.Float(string=u'Activity Count', )

    rate = fields.Float(string=u'Rate', compute='_compute_rate')

    object_distribution_ids = fields.One2many(
        string=u'Object Distribution',
        comodel_name='account.costing.abc.plan.object.distribution',
        inverse_name='distribution_id',
    )

    @api.depends('percent', 'activity')
    def _compute_rate(self):
        for record in self:
            record.cost = float(record.plan_id.amount * record.percent)

            if record.activity_id.value and record.activity > 0:
                record.rate = float(record.cost / record.activity)
            else:
                record.rate = 0

    def action_show_details(self):

        self.ensure_one()

        view = self.env.ref(
            'account_cost_abc.view_form_abc_plan_activity_distribution'
        )

        return {
            'name': _('Detailed Operations'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.costing.abc.plan.activity.distribution',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(self.env.context, ),
        }


class CostingPlanObjectDistribution(models.Model):
    _name = 'account.costing.abc.plan.object.distribution'
    _description = 'Costing Plan Object Distribution'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string=u'Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    distribution_id = fields.Many2one(
        string=u'Plan',
        comodel_name='account.costing.abc.plan.activity.distribution',
        ondelete='restrict',
    )

    product_id = fields.Many2one(
        string=u'Product', comodel_name='product.product', required=True
    )

    partner_id = fields.Many2one(
        string=u'Partner',
        comodel_name='res.partner',
    )

    activity_id = fields.Many2one(
        string=u'Activity',
        comodel_name='account.cost.activity',
        ondelete='restrict',
    )

    activity = fields.Float(string=u'Activity', required=True)

    amount = fields.Float(string=u'Amount', compute='_compute_amount')

    @api.depends('activity', 'distribution_id.rate')
    def _compute_amount(self):
        for record in self:
            record.amount = record.activity * record.distribution_id.rate


class AccountCostResult(models.Model):
    _name = 'account.cost.result'
    _description = 'Account Cost Result'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string=u'Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    plan_id = fields.Many2one(
        string=u'Plan',
        comodel_name='account.costing.abc.plan',
        ondelete='restrict',
    )

    product_id = fields.Many2one(
        string=u'Product',
        comodel_name='product.product',
    )

    partner_id = fields.Many2one(
        string=u'Partner',
        comodel_name='res.partner',
    )

    distribution_ids = fields.One2many(
        string=u'Distribution',
        comodel_name='account.costing.abc.plan.object.distribution',
        compute='_compute_distribution_ids'
    )

    @api.depends('partner_id', 'partner_id')
    def _compute_distribution_ids(self):
        for record in self:
            if record.product_id:

                record.distribution_ids = self.env[
                    'account.costing.abc.plan.object.distribution'].search(
                        [
                            ('partner_ids', 'in', record.partner_id.ids),
                            ('distribution_id.plan_id', '=', record.plan_id)
                        ]
                    )

            elif not record.partner_id and record.partner_id:
                record.distribution_ids = self.env[
                    'account.costing.abc.plan.object.distribution'].search(
                        [
                            ('partner_ids', 'in', record.partner_id.ids),
                            ('distribution_id.plan_id', '=', record.plan_id)
                        ]
                    )

            else:
                record.distribution_ids = None

    cost = fields.Float(string=u'Cost', compute='_compute_cost')

    @api.depends('distribution_ids')
    def _compute_cost(self):
        for record in self:
            record.cost = sum(record.distribution_ids.mapped('amount'))
