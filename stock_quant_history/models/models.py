# -*- coding: utf-8 -*-

from odoo import models, fields, api
import ast


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        check_company=True,
        domain=[('usage', '=', 'internal')]
    )

    def open_at_date(self):
        action = super(StockQuantityHistory, self).open_at_date()
        origin_ctx = action.get('context')
        if isinstance(action.get('context'), str):
            origin_ctx = ast.literal_eval(action.get('context'))

        if self.location_id:
            origin_ctx.update({'location': self.location_id.id})
            action.update({'context': origin_ctx})

        return action
