from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    restrict_lot_id = fields.Many2one(
        'stock.production.lot',
        string='Restricted Lot Numbers',
        readonly=False
    )

    def _get_available_quantity(
        self,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        allow_negative=False
    ):
        self.ensure_one()
        if self.restrict_lot_id:
            lot_id = self.restrict_lot_id
            # strict = True

        return super(StockMove, self)._get_available_quantity(
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
            allow_negative=allow_negative
        )
