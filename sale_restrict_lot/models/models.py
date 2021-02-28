from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    restrict_lot_id = fields.Many2one(
        'stock.production.lot',
        string='Restricted Lot Numbers',
        related="order_line.restrict_lot_id"
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    restrict_lot_id = fields.Many2one(
        'stock.production.lot',
        string='Restricted Lot Numbers',
        readonly=False
    )


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['restrict_lot_id']
        return fields
